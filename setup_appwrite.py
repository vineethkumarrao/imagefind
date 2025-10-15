"""
Setup script for Appwrite resources
Creates database, collection, and storage buckets
"""

import os
import sys
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.permission import Permission
from appwrite.role import Role
from config import config

def setup_appwrite():
    """Setup Appwrite database, collection, and storage buckets"""
    
    print("🚀 Starting Appwrite setup...")
    print(f"📍 Endpoint: {config.APPWRITE_ENDPOINT}")
    print(f"🔑 Project ID: {config.APPWRITE_PROJECT_ID}")
    
    try:
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(config.APPWRITE_ENDPOINT)
        client.set_project(config.APPWRITE_PROJECT_ID)
        client.set_key(config.APPWRITE_API_KEY)
        
        # Initialize services
        databases = Databases(client)
        storage = Storage(client)
        
        # Step 1: Create Database
        print("\n📚 Creating database...")
        try:
            database = databases.create(
                database_id=config.APPWRITE_DATABASE_ID,
                name='Quantum Images Database'
            )
            print(f"Database created: {database['$id']}")
        except Exception as e:
            if 'already exists' in str(e).lower() or 'document already exists' in str(e).lower():
                print(f"ℹ️  Database already exists: {config.APPWRITE_DATABASE_ID}")
            else:
                print(f"Database creation error: {e}")
        
        # Step 2: Create Collection
        print("\n📋 Creating collection...")
        try:
            collection = databases.create_collection(
                database_id=config.APPWRITE_DATABASE_ID,
                collection_id=config.APPWRITE_COLLECTION_ID,
                name='Feature Vectors',
                permissions=[
                    Permission.read(Role.any()),
                    Permission.create(Role.any()),
                    Permission.update(Role.any()),
                    Permission.delete(Role.any())
                ]
            )
            print(f"Collection created: {collection['$id']}")
            
            # Step 3: Create Attributes
            print("\n🏗️  Creating collection attributes...")
            
            # image_id (string, required, unique)
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='image_id',
                    size=255,
                    required=True
                )
                print("Created attribute: image_id")
            except Exception as e:
                print(f"ℹ️  image_id: {e}")
            
            # category (string, required)
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='category',
                    size=50,
                    required=True
                )
                print("Created attribute: category")
            except Exception as e:
                print(f"ℹ️  category: {e}")
            
            # features (string, required) - JSON array stored as string
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='features',
                    size=10000,
                    required=True
                )
                print("Created attribute: features")
            except Exception as e:
                print(f"ℹ️  features: {e}")
            
            # filename (string, required)
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='filename',
                    size=255,
                    required=True
                )
                print("Created attribute: filename")
            except Exception as e:
                print(f"ℹ️  filename: {e}")
            
            # storage_path (string, required)
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='storage_path',
                    size=500,
                    required=True
                )
                print("Created attribute: storage_path")
            except Exception as e:
                print(f"ℹ️  storage_path: {e}")
            
            # bucket_id (string, required)
            try:
                databases.create_string_attribute(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='bucket_id',
                    size=100,
                    required=True
                )
                print("Created attribute: bucket_id")
            except Exception as e:
                print(f"ℹ️  bucket_id: {e}")
            
            # Create indexes
            print("\nCreating indexes...")
            try:
                databases.create_index(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='category_index',
                    type='key',
                    attributes=['category']
                )
                print("Created index: category_index")
            except Exception as e:
                print(f"ℹ️  category_index: {e}")
            
            try:
                databases.create_index(
                    database_id=config.APPWRITE_DATABASE_ID,
                    collection_id=config.APPWRITE_COLLECTION_ID,
                    key='image_id_index',
                    type='unique',
                    attributes=['image_id']
                )
                print("Created index: image_id_index")
            except Exception as e:
                print(f"ℹ️  image_id_index: {e}")
            
        except Exception as e:
            if 'already exists' in str(e).lower() or 'document already exists' in str(e).lower():
                print(f"ℹ️  Collection already exists: {config.APPWRITE_COLLECTION_ID}")
            else:
                print(f"Collection creation error: {e}")
        
        # Step 4: Create Storage Buckets
        print("\nCreating storage buckets...")
        
        buckets = [
            (config.APPWRITE_BUCKET_HEALTHCARE, 'Healthcare Images'),
            (config.APPWRITE_BUCKET_SATELLITE, 'Satellite Images'),
            (config.APPWRITE_BUCKET_SURVEILLANCE, 'Surveillance Images')
        ]
        
        for bucket_id, bucket_name in buckets:
            try:
                bucket = storage.create_bucket(
                    bucket_id=bucket_id,
                    name=bucket_name,
                    permissions=[
                        Permission.read(Role.any()),
                        Permission.create(Role.any()),
                        Permission.update(Role.any()),
                        Permission.delete(Role.any())
                    ],
                    file_security=False,
                    enabled=True,
                    maximum_file_size=30000000,  # 30MB
                    allowed_file_extensions=[],
                    compression='gzip',
                    encryption=True,
                    antivirus=True
                )
                print(f"Created bucket: {bucket_name} ({bucket_id})")
            except Exception as e:
                if 'already exists' in str(e).lower() or 'document already exists' in str(e).lower():
                    print(f"ℹ️  Bucket already exists: {bucket_name} ({bucket_id})")
                else:
                    print(f"Bucket creation error for {bucket_name}: {e}")
        
        print("\n✨ Appwrite setup completed successfully!")
        print(f"\nSummary:")
        print(f"   Database ID: {config.APPWRITE_DATABASE_ID}")
        print(f"   Collection ID: {config.APPWRITE_COLLECTION_ID}")
        print(f"   Healthcare Bucket: {config.APPWRITE_BUCKET_HEALTHCARE}")
        print(f"   Satellite Bucket: {config.APPWRITE_BUCKET_SATELLITE}")
        print(f"   Surveillance Bucket: {config.APPWRITE_BUCKET_SURVEILLANCE}")
        print(f"\n🌐 Visit your Appwrite Console:")
        print(f"   {config.APPWRITE_ENDPOINT.replace('/v1', '/console')}")
        
        return True
        
    except Exception as e:
        print(f"\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        config.validate()
        success = setup_appwrite()
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
