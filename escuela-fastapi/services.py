import boto3
import uuid
import time
import secrets
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from tables import AlumnoDB, ProfesorDB
from models import AlumnoCreate, ProfesorCreate
from botocore.exceptions import ClientError

load_dotenv()

s3_client = boto3.client('s3', region_name=os.getenv("S3_REGION", "us-east-1"))
sns_client = boto3.client('sns', region_name=os.getenv("SNS_REGION", "us-east-1"))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("DYNAMODB_REGION", "us-east-1"))

BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "tu-bucket-nombre")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:tu-topic")
DYNAMO_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "sesiones-alumnos")

class AlumnoService:
    def get_all(self, db: Session):
        return db.query(AlumnoDB).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(AlumnoDB).filter(AlumnoDB.id == id).first()

    def create(self, db: Session, data: AlumnoCreate):
        nuevo_alumno = AlumnoDB(**data.dict())
        db.add(nuevo_alumno)
        db.commit()
        db.refresh(nuevo_alumno)
        return nuevo_alumno

    def update(self, db: Session, id: int, data: AlumnoCreate):
        alumno = db.query(AlumnoDB).filter(AlumnoDB.id == id).first()
        if not alumno:
            return None
        for key, value in data.dict().items():
            setattr(alumno, key, value)
        db.commit()
        db.refresh(alumno)
        return alumno

    def delete(self, db: Session, id: int):
        alumno = db.query(AlumnoDB).filter(AlumnoDB.id == id).first()
        if not alumno:
            return False
        db.delete(alumno)
        db.commit()
        return True

    # --- AWS INTEGRATIONS ---
    
    def upload_photo(self, db: Session, id: int, file):
        alumno = self.get_by_id(db, id)
        if not alumno:
            return None
        
        try:
            if not file or not file.filename:
                print("Error: No file provided or filename is empty")
                return None
            
            file_key = f"fotos/{id}/{file.filename}"
            
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=file_key,
                Body=file_content,
                ContentType=file.content_type,
                ACL='public-read'
            )
            
            url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_key}"
            alumno.fotoPerfilUrl = url
            db.commit()
            db.refresh(alumno)
            return url
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in upload_photo: {e}")
            return None

    def send_email_notification(self, db: Session, id: int):
        alumno = self.get_by_id(db, id)
        if not alumno:
            return False
        
        try:
            message = f"Información del Alumno:\nNombre: {alumno.nombres} {alumno.apellidos}\nMatrícula: {alumno.matricula}\nPromedio: {alumno.promedio}"
            
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject=f"Notificación de Calificaciones - {alumno.nombres} {alumno.apellidos}"
            )
            return True
        except ClientError as e:
            print(f"Error sending SNS notification: {e}")
            return False

    def login(self, db: Session, id: int, password: str):
        alumno = self.get_by_id(db, id)
        if not alumno or alumno.password != password:
            return None
            
        session_string = secrets.token_hex(64)
        try:
            table = dynamodb.Table(DYNAMO_TABLE_NAME)
            item = {
                'id': str(uuid.uuid4()),
                'fecha': int(time.time()),
                'alumnoId': id,
                'active': True,
                'sessionString': session_string
            }
            table.put_item(Item=item)
            return session_string
        except ClientError as e:
            print(f"Error writing to DynamoDB: {e}")
            return None

    def verify_session(self, id: int, session_string: str):
        try:
            table = dynamodb.Table(DYNAMO_TABLE_NAME)
            
            from boto3.dynamodb.conditions import Attr, And
            
            response = table.scan(
                FilterExpression=And(Attr('sessionString').eq(session_string), 
                                     Attr('alumnoId').eq(id))
            )
            
            items = response.get('Items', [])
            if not items:
                return False
                
            session = items[0]
            return session.get('active', False)
        except ClientError as e:
            print(f"Error verifying session: {e}")
            return False

    def logout(self, id: int, session_string: str):
        try:
            table = dynamodb.Table(DYNAMO_TABLE_NAME)
            
            from boto3.dynamodb.conditions import Attr, And
            
            # Buscar el item primero para obtener su Primary Key (id)
            response = table.scan(
                 FilterExpression=And(Attr('sessionString').eq(session_string), 
                                      Attr('alumnoId').eq(id))
            )
            items = response.get('Items', [])
            if not items:
                return False
                
            primary_key = items[0]['id']
            
            table.update_item(
                Key={'id': primary_key},
                UpdateExpression="set active = :a",
                ExpressionAttributeValues={':a': False}
            )
            return True
        except ClientError as e:
            print(f"Error logging out: {e}")
            return False

class ProfesorService:
    def get_all(self, db: Session):
        return db.query(ProfesorDB).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(ProfesorDB).filter(ProfesorDB.id == id).first()

    def create(self, db: Session, data: ProfesorCreate):
        nuevo = ProfesorDB(**data.dict())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    def update(self, db: Session, id: int, data: ProfesorCreate):
        profe = db.query(ProfesorDB).filter(ProfesorDB.id == id).first()
        if not profe: return None
        for key, value in data.dict().items():
            setattr(profe, key, value)
        db.commit()
        db.refresh(profe)
        return profe

    def delete(self, db: Session, id: int):
        profe = db.query(ProfesorDB).filter(ProfesorDB.id == id).first()
        if not profe: return False
        db.delete(profe)
        db.commit()
        return True
