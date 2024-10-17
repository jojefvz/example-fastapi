from typing import List, Optional

from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int=Depends(oauth2.get_current_user),
    limit: int=10,
    skip: int=0,
    search: Optional[str]=''):
    
    results = (db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
     .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
     .group_by(models.Post.id)
     .filter(models.Post.title.contains(search))
     .limit(limit)
     .offset(skip)
     .all())
    
    results = list(map(lambda x: x._mapping, results))
    return results

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session =Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = (db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
     .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
     .group_by(models.Post.id)
     .filter(models.Post.id == id)
     .first())
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/{id}')
def update_post(new_post: schemas.PostCreate, id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')
    
    if query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized to perform requested action.')
    
    new_post = new_post.model_dump()
    query.update(new_post, synchronize_session=False)
    db.commit()
    return query.first()
    
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} does not exist.')
    
    if query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized to perform requested action.')
    
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
