from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Definition of the Word class


class Word(BaseModel):
    word: str
    requested: int = 0


# Pseudo database with some initial records
word_records = [
    Word(word="Apfel"),
    Word(word="Auto"),
    Word(word="Berlin")]

# Here begins the API definition part

app = FastAPI(title="FastAPI Words", version="0.0.1")

# The root endpoint


@app.get("/")
async def root():
    return {"message": "Hello from the Words API"}

# The endpoint to get all words


@app.get("/words")
async def get_all_words():
    for record in word_records:
        record.requested += 1
    return word_records

# The endpoint to get one word


@app.get("/words/{word}")
async def get_one_word(word: str):

    for record in word_records:
        if record.word == word:
            record.requested += 1
            return record

    raise HTTPException(status_code=404, detail=f"Word '{word}' not found")

# The endpoint to create a new word


@app.post("/words")
async def create_word(word: Word):
    word_records.append(word)
    return word

# The endpoint to delete a word


@app.delete("/words/{word}")
async def delete_word(word: str):
    global word_records
    deleted_word_count = 0
    word_records_new = []
    for record in word_records:
        if record.word == word:
            deleted_word_count += 1
            continue
        word_records_new.append(record)

    if deleted_word_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Word '{word}' not found in List of Words")

    word_records = word_records_new
    return {"message": f"{deleted_word_count} record(s) deleted"}
