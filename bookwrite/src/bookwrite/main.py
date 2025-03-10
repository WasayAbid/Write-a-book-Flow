#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from bookwrite.crews.book_writer_crew.book_writer_crew import BookWriterCrew


class BookState(BaseModel):
    chapter_count: int = 1
    outline: str = ""
    chapters: list = []
    edited_chapters: list = []


class BookWriterFlow(Flow[BookState]):

    @start()
    def generate_chapter_count(self):
        print("Setting chapter count to 1")
        self.state.chapter_count = 1  # Let's generate 5-10 chapters

    @listen(generate_chapter_count)
    def create_outline(self):
        print("Creating outline")
        result = (
            BookWriterCrew()
            .crew()
            .kickoff(inputs={"chapter_count": self.state.chapter_count})
        )

        print("Outline created", result.raw)
        self.state.outline = result.raw

    @listen(create_outline)
    def write_chapters(self):
        print("Writing chapters")
        for chapter in range(self.state.chapter_count):
            result = (
                BookWriterCrew()
                .crew()
                .kickoff(inputs={"chapter": chapter, "outline": self.state.outline})
            )
            self.state.chapters.append(result.raw)
            print(f"Chapter {chapter+1} written")

    @listen(write_chapters)
    def edit_chapters(self):
        print("Editing chapters")
        for chapter in self.state.chapters:
            result = (
                BookWriterCrew()
                .crew()
                .kickoff(inputs={"chapter": chapter})
            )
            self.state.edited_chapters.append(result.raw)
            print("Chapter edited")

    @listen(edit_chapters)
    def save_book(self):
        print("Saving book")
        with open("book.txt", "w") as f:
            f.write("\n\n".join(self.state.edited_chapters))


def kickoff():
    book_writer_flow = BookWriterFlow()
    book_writer_flow.kickoff()


