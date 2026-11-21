"""quiz.py - 퀴즈 한 문제를 표현하는 Quiz 클래스

역할: 문제 출력, 정답 판정, 저장용 변환만 담당한다.
(사용자 입력을 받는 일은 QuizGame 클래스가 맡는다.)
"""


class Quiz:
    """퀴즈 한 문제 (문제, 선택지 4개, 정답 번호 1~4)"""

    def __init__(self, question, choices, answer):
        # 속성(attribute): 이 퀴즈가 가지고 있는 데이터
        self.question = question    # 문제 글자 (str)
        self.choices = choices      # 선택지 4개 (list of str)
        self.answer = answer        # 정답 번호 1~4 (int) - 리스트 인덱스(0~3)가 아님에 주의

    def display(self, number):
        """문제와 선택지를 화면에 출력한다. number는 '몇 번째 문제'인지."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        # enumerate(start=1): 선택지에 1, 2, 3, 4 번호를 붙여 준다
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답이면 True, 아니면 False"""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 파일에 저장할 수 있게 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리(JSON에서 읽은 데이터)를 Quiz 객체로 되돌린다.

        self가 없는 이유: 아직 Quiz 객체가 없는 상태에서 객체를 '만들어 주는' 함수이기 때문.
        데이터가 이상하면(키 없음, 선택지 4개 아님, 정답 범위 밖) 오류를 일으켜서
        QuizGame이 '파일 손상'으로 처리할 수 있게 한다.
        """
        question = data["question"]      # 키가 없으면 KeyError
        choices = data["choices"]
        answer = data["answer"]

        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 값이 올바르지 않습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개짜리 리스트여야 합니다.")
        if not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("answer는 1~4 사이의 정수여야 합니다.")

        return Quiz(question, choices, answer)


# 이 파일만 직접 실행(python quiz.py)했을 때만 동작하는 간단 테스트
# (다른 파일에서 import 할 때는 실행되지 않는다)
if __name__ == "__main__":
    q = Quiz("Python의 창시자는?", ["Guido", "Linus", "Bjarne", "James"], 1)
    q.display(1)
    print("1번 선택 →", q.is_correct(1))   # True
    print("2번 선택 →", q.is_correct(2))   # False

    data = q.to_dict()
    print("딕셔너리 변환 →", data)
    q2 = Quiz.from_dict(data)
    print("복원한 문제 →", q2.question)