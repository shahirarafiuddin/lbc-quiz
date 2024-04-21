from abc import ABC, abstractmethod


class Question(ABC):
  """
  This is the abstract Question class, it's not designed to be used
  directly and instead should be implemented via the subclasses.

  It has two methods that the subclasses must implement:
    1. display(): Displays the question to the user and prompts for answer
    2. check_answer(): Checks the user's answer and returns a boolean

  From this abstract class, we can create multiple formats of
  questions that share the same underpinnings.
  """

  @abstractmethod
  def display(self):
    """
    This method is used to display the question and prompt the user for an answer
    """
    ...

  @abstractmethod
  def check_answer(self) -> bool:
    """
    This method is used to check the answer of the question
    """
    ...


class ObjectiveQuestion(Question):
  """
  This class is used to create a question with a y/n answer
  """

  def __init__(self, prompt: str, correct_answer: bool):
    """
    It accepts the following arguments:
      1. prompt: the question to be asked
      2. correct_answer: the correct answer to the question
    """
    self.prompt = prompt
    self.correct_answer = correct_answer
    self.answer = None

  def display(self):
    """
    This method is used to display the question and prompt the user for an answer
    """
    print(self.prompt)
    self.prompt_answer()

  def prompt_answer(self):
    """
    This method is used to prompt the user for an answer
    """
    answer = input("Enter your answer (y/n): ")

    # Check if the answer is valid using pattern matching
    # conditional check
    # we lowercased the answer to make it case insensitive
    match answer.lower():
      case "y":
        # set the answer to True
        self.answer = True
      case "n":
        # set the answer to False
        self.answer = False
      case _:
        # if the answer does not match any of the cases
        # display an error message
        # re-prompt the user for an answer
        print("Invalid answer. Please enter 'y' or 'n'.")
        return self.prompt_answer()

  def check_answer(self):
    """
    This method is used to check the answer of the question
    """
    return self.answer == self.correct_answer

class DumbQuestion(Question):
  """
  This is a silly question implementation that implements the basic shape of a Question
  without much logic in it.
  """
  
  def display(self):
    print("This is a dumb question")
    input("Answer something, it doesn't matter:")

  def check_answer(self):
    return True

class MultipleChoiceQuestion(Question):
  """
  This is a class to create a multiple choice question
  """

  def __init__(self, prompt: str, choices: list[str], correct_answer: str):
    """
    It accepts the following arguments:
      1. prompt: the question to be asked
      2. correct_answer: the correct answer to the question
      3. choices: a list of choices for the question
    """
    self.prompt = prompt
    self.correct_answer = correct_answer
    self.choices = choices

  def display(self):
    """
    This method displays the question and its choices
    """
    print(self.prompt)
    self.prompt_answer()

  def prompt_answer(self):
    """
    Prompts the user to enter their answer and checks if it is correct.
    """
    # loops through the choices and displays them in the following format:
    # 1. choice1
    # 2. choice2
    # etc...
    for i, choice in enumerate(self.choices):
      print(f"{i+1}. {choice}")

    # prompts the user to enter their answer
    answer = input(f"Enter your answer (1-{len(self.choices)}): ")

    try:
      # convert the answer to an integer
      # may throw a ValueError if the input is not a number
      answer = int(answer)

      # check if the answer is within the range of choices
      if answer < 1 or answer > len(self.choices):
        # if the answer is not within the range of choices
        # raise a ValueError
        raise ValueError

      # get the correct answer index
      # since arrays are indexed from 0, we need to subtract 1
      # from the answer to get the correct index
      self.answer = self.choices[answer - 1]
    except ValueError:
      # if the answer is not valid
      # re-prompt the user for input
      # we use the len method to get the number of choices avaiable
      # for this question
      print(
          f"Invalid answer. Please enter a number between 1 and {len(self.choices)}."
      )
      return self.prompt_answer()

  def check_answer(self):
    """
    Checks if the user's answer is correct.
    """
    return self.answer == self.correct_answer


class Quiz:
  """
  This class is used to create a quiz
  """

  def __init__(self, intro):
    self.questions = []
    self.score = 0
    self.intro = intro

  def add_question(self, question: Question):
    """
    This method is used to add a question to the quiz.
    It accepts the following argument:
      1. question: the question to be added to the quiz, must be of type Question or 
      it's subclasses (ObjectiveQuestion or MultipleChoiceQuestion))
    """
    self.questions.append(question)

  def run(self):
    """
    This method is used to run the quiz.
    It loops through each question in the quiz and uses the Question abstract methods to
    display and check the answer.
    """
    # display the quiz intro
    print(self.intro)

    # loop through each question in the quiz
    for question in self.questions:
      # display the question and prompt the user for an answer
      question.display()
      # print a blank line between each question
      print("")

      # check the answer
      if question.check_answer():
        # if the answer is correct, increment the score
        self.score += 1

    # display the final score when the quiz is complete
    print("=== Results ===")
    print(f"Your score is {self.score} out of {len(self.questions)}\n\n")


if __name__ == "__main__":
  """
  This statement checks if the script is being run as the main program
  this is to differentiate a python program from a module that 
  is being imported into another script
  """

  # create a list to contain the quizzes
  quizzes = []

  # create a quiz with an intro
  bio_quiz = Quiz("""Welcome to the Biology Quiz!

This quiz contains 10 questions about biology in two formats:
  1. Objective questions
  2. Multiple choice questions

Please spend no more than 10 minutes on this quiz.
---
""")

  # add a question to the quiz
  bio_quiz.add_question(
    MultipleChoiceQuestion(
      "What do plants need for growth?",
      ["water/sunlight", "food", "coffee", "rain"],
      "water/sunlight",
    )
  )

  # mix it up with another question type
  bio_quiz.add_question(
    ObjectiveQuestion("Is the sky blue?", True)
  )

  # append the quiz to the quizzes list
  quizzes.append(bio_quiz)

  # create another quiz with an intro
  math_quiz = Quiz("""Welcome to the Math Quiz!

This quiz contains 10 questions in the objective format.

Please spend no more than 10 minutes on this quiz.
---
""")

  # add a question to the quiz
  math_quiz.add_question(
    ObjectiveQuestion("Is 1+1=2", True)
  )
  math_quiz.add_question(
    ObjectiveQuestion("Is 4-2=2", True)
  )
  math_quiz.add_question(
    DumbQuestion()
  )

  # append another quiz to the quizzes list
  quizzes.append(math_quiz)

  # loop through the quizzes and run them
  for quiz in quizzes:
    quiz.run()
