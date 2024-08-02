from app import db, create_app
from models import User, Artwork, Gallery, Order
from werkzeug.security import generate_password_hash
from datetime import datetime


app = create_app()
app.app_context().push()


def seed():
   
    db.drop_all()
    db.create_all()

  
    admin = User(
        username='admin', 
        email='admin@example.com', 
        password_hash=generate_password_hash('password'), 
        role='admin'
    )
    artist = User(
        username='artist', 
        email='artist@example.com', 
        password_hash=generate_password_hash('password'), 
        role='artist'
    )
    viewer = User(
        username='viewer', 
        email='viewer@example.com', 
        password_hash=generate_password_hash('password'), 
        role='viewer'
    )

    db.session.add(admin)
    db.session.add(artist)
    db.session.add(viewer)
    db.session.commit()  

   
    gallery = Gallery(
        name='Modern Art', 
        description='A gallery of modern art pieces', 
        admin_id=admin.id
    )
    db.session.add(gallery)
    db.session.commit()  

    artwork1 = Artwork(
        title='Abstract Painting', 
        description='A beautiful abstract painting', 
        artist_id=artist.id, 
        price=200.0, 
        gallery_id=gallery.id
    )
    artwork2 = Artwork(
        title='Modern Sculpture', 
        description='A contemporary sculpture', 
        artist_id=artist.id, 
        price=500.0, 
        gallery_id=gallery.id
    )

    db.session.add(artwork1)
    db.session.add(artwork2)
    db.session.commit() 

    
    order1 = Order(
        artwork_id=artwork1.id,
        buyer_id=viewer.id,
        status='Pending',
        total_price=artwork1.price,
        created_at=datetime.utcnow(),
        digital_certificate='https://example.com/cert1'
    )

    order2 = Order(
        artwork_id=artwork2.id,
        buyer_id=viewer.id,
        status='Completed',
        total_price=artwork2.price,
        created_at=datetime.utcnow(),
        digital_certificate='https://example.com/cert2'
    )

    db.session.add(order1)
    db.session.add(order2)
    db.session.commit() 


    print("Database seeded with initial data.")

if __name__ == '__main__':
    seed()
