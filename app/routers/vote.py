from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import oauth2, schemas, models
from ..database import get_db

router = APIRouter(prefix='/votes', tags=['Votes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {vote.post_id} does not exist.')
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, 
                                              models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'User id: {current_user.id} has already voted for post id: {vote.post_id}.')
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'Vote does not exist.')
            
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted."}