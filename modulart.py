import sqlite3 as sql

from functools import wraps
from flask import session,flash,redirect,url_for


connect_db ='project.db'


def countartist():
    with sql.connect(connect_db) as db:
        qry = 'select count (*) from artist'
        result=db.execute(qry)
        return(result)

def result():
    rows=list_artist()
    list_gallery() 
    for row in rows:
        print(row)

def list_artwork1():
    with sql.connect(connect_db) as db:
        qry = 'select artwork.artwork_id, artwork.title, artist.artist_name, gallery.gallery_name,artwork.year, artwork.picture_name from artwork, artist, gallery where artwork.artist_id = artist.artist_id and artwork.gallery_id = gallery.gallery_id ' 
        result=db.execute(qry)
        return(result)
    
def list_artist():
  with sql.connect(connect_db) as db:
    qry = 'select * from artist' 
    result=db.execute(qry)
    return(result)
    
def list_gallery():
  with sql.connect(connect_db) as db:
    qry = 'select * from gallery' 
    result=db.execute(qry)
    return(result)

def list_artwork():
  with sql.connect(connect_db) as db:
    qry = 'select * from artwork' 
    result=db.execute(qry)
    return(result)

def find_artist(artist_id):
  with sql.connect(connect_db) as db:
    qry = 'select * from artist where artist_id=?'
    result=db.execute(qry,(artist_id,)).fetchone()
    return(result)


def find_gallery(gallery_id):
  with sql.connect(connect_db) as db:
    qry = 'select * from gallery where gallery_id=?'
    result=db.execute(qry,(gallery_id,)).fetchone()
    return(result)

def find_artwork(artwork_id):
  with sql.connect(connect_db) as db:
    qry = 'select * from artwork where artwork_id=?'
    result=db.execute(qry,(artwork_id,)).fetchone()
    return(result)

def find_artwork1(artist_id):
  with sql.connect(connect_db) as db:
    qry = 'select * from artwork where artist_id=?'
    result=db.execute(qry,(artist_id,))
    return(result)
    
def find_staff(username):
  with sql.connect(connect_db) as db:
    qry = 'select * from admin where username=?'
    result=db.execute(qry,(username,)).fetchone()
    return(result)

def insert_artist(artist_id,artist_name,artist_style,birthplace,dob,age):
  with sql.connect(connect_db) as db:
    qry='insert into artist (artist_id,artist_name,artist_style,birthplace,dob,age) values (?,?,?,?,?,?)' 
    db.execute(qry,(artist_id,artist_name,artist_style,birthplace,dob,age))
    
def insert_gallery(gallery_id,gallery_name,address,contact):
  with sql.connect(connect_db) as db:
    qry='insert into gallery (gallery_id,gallery_name,address,contact) values (?,?,?,?)' 
    db.execute(qry,(gallery_id,gallery_name,address,contact))
    
def insert_artwork(artwork_id,title,artwork_type,year,artist_id,gallery_id,picture_name):
  with sql.connect(connect_db) as db:
    qry='insert into artwork (artwork_id,title,artwork_type,year,artist_id,gallery_id,picture_name) values (?,?,?,?,?,?,?)' 
    db.execute(qry,(artwork_id,title,artwork_type,year,artist_id,gallery_id,picture_name))
    
def insert_staff(username,password):
  with sql.connect(connect_db) as db:
    qry='insert into admin (username,password) values (?,?)' 
    db.execute(qry,(username,password))
    
def update_artist(artist_name,artist_style,birthplace,dob,age,artist_id):
  with sql.connect(connect_db) as db:
    qry='update artist set artist_name=?,artist_style=?,birthplace=?,dob=?,age=? where artist_id=?' 
    db.execute(qry, (artist_name,artist_style,birthplace,dob,age,artist_id))
    
def update_gallery(gallery_name,address,contact,gallery_id):
  with sql.connect(connect_db) as db:
    qry='update gallery set gallery_name=?,address=?,contact=? where gallery_id=?' 
    db.execute(qry, (gallery_name,address,contact,gallery_id))
    
def update_artwork(title,artwork_type,year,artist_id,gallery_id,picture,artwork_id):
  with sql.connect(connect_db) as db:
    qry='update artwork set title=?,artwork_type=?,year=?,artist_id=?,gallery_id=?,picture_name=? where artwork_id=?' 
    db.execute(qry, (title,artwork_type,year,artist_id,gallery_id,picture,artwork_id))
    
def update_staff(password,username):
  with sql.connect(connect_db) as db:
    qry='update admin set password=? where username=?' 
    db.execute(qry, (password,username))

def delete_artist(artist_id):
  with sql.connect(connect_db) as db:
    qry='delete from artist where artist_id=?' 
    db.execute(qry,(artist_id,))
    
def delete_gallery(gallery_id):
  with sql.connect(connect_db) as db:
    qry='delete from gallery where gallery_id=?' 
    db.execute(qry,(gallery_id,))
    
def delete_artwork(artwork_id):
  with sql.connect(connect_db) as db:
    qry='delete from artwork where artwork_id=?' 
    db.execute(qry,(artwork_id,))

    
def check_artist_id(artist_id):
  with sql.connect(connect_db) as db: 
    qry = 'select artist_id from artist where artist_id=?'
    result=db.execute(qry,(artist_id,)).fetchone()
    return(result)

def check_gallery_id(gallery_id):
  with sql.connect(connect_db) as db: 
    qry = 'select gallery_id from gallery where gallery_id=?'
    result=db.execute(qry,(gallery_id,)).fetchone()
    return(result)
    
def check_artwork_id(artwork_id):
  with sql.connect(connect_db) as db: 
    qry = 'select artwork_id from artwork where artwork_id=?'
    result=db.execute(qry,(artwork_id,)).fetchone()
    return(result)

def check_admin(username):
  with sql.connect(connect_db) as db: 
    qry = 'select username from admin where username=?'
    result=db.execute(qry,(username,)).fetchone()
    return(result)

def checklogin(username,password):
    with sql.connect(connect_db) as db: 
        qry = 'select username,password from admin where username=? and password=?'
        result=db.execute(qry,(username,password)).fetchone()
        return(result)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('admin'))
        return wrap