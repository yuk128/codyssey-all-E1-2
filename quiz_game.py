"""quiz_game.py - 게임 전체를 관리하는 QuizGame 클래스

역할: 메뉴, 입력 처리, 퀴즈 풀기/추가/목록/점수, 파일 저장/불러오기
(퀴즈 한 문제에 대한 일은 quiz.py의 Quiz 클래스가 맡는다.)
"""

import json

from quiz import Quiz

STATE_FILE = "state.json"   # 저장 파일 이름 (프로젝트 루트). 한 곳에서만 정의해 둔다.
LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        # 속성: 퀴즈 목록(Quiz 객체들의 리스트), 최고 점수(없으면 None)
        self.quizzes = []
        self.best_score = None
        # 객체를 만들자마자 저장된 데이터를 불러온다
        self.load_state()

    # ------------------------------------------------------------------
    # 1. 기본 퀴즈 데이터
    # ------------------------------------------------------------------
    def get_default_quizzes(self):
        """기본 퀴즈 6개를 Quiz 객체로 만들어 리스트로 돌려준다.
        주제: 파이썬/Git 기초  (← 본인이 고른 주제로 바꿔도 된다)
        """
        return [
            Quiz("Python 언어를 만든 사람은?",
                 ["귀도 반 로섬", "리누스 토르발즈", "비야네 스트롭스트룹", "제임스 고슬링"], 1),
            Quiz("리스트의 맨 끝에 값을 추가하는 메서드는?",
                 ["add()", "append()", "push()", "insert_last()"], 2),
            Quiz("'이름: 값' 형태의 쌍으로 데이터를 저장하는 자료형은?",
                 ["list", "tuple", "dict", "set"], 3),
            Quiz("클래스로 객체를 만들 때 자동으로 호출되는 메서드는?",
                 ["__start__", "__new_obj__", "__init__", "__main__"], 3),
            Quiz("내 컴퓨터의 커밋을 GitHub 같은 원격 저장소에 올리는 명령어는?",
                 ["git pull", "git push", "git clone", "git merge"], 2),
            Quiz("print(type(3.14)) 를 실행하면 나오는 자료형은?",
                 ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"], 2),
        ]

    # ------------------------------------------------------------------
    # 2. 입력 처리 (공통 함수) - 메뉴/정답/정답번호 입력에서 모두 재사용
    # ------------------------------------------------------------------
    def read_int(self, prompt, min_value, max_value):
        """min_value~max_value 사이의 정수를 입력받을 때까지 반복한다.

        처리하는 경우: 앞뒤 공백, 빈 입력, 숫자가 아닌 입력, 범위 밖 숫자
        (Ctrl+C / EOF 는 여기서 처리하지 않고 run()에서 한꺼번에 처리한다.)
        """
        while True:
            text = input(prompt).strip()          # 앞뒤 공백 제거

            if text == "":                         # 빈 입력(그냥 Enter)
                print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            try:
                number = int(text)                 # 숫자 변환 (abc 면 ValueError)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not min_value <= number <= max_value:   # 범위 밖
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def read_text(self, prompt):
        """비어 있지 않은 글자를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 빈 입력입니다. 내용을 입력해 주세요.")
                continue
            return text

    # ------------------------------------------------------------------
    # 3. 화면 출력
    # ------------------------------------------------------------------
    def show_menu(self):
        print()
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    # ------------------------------------------------------------------
    # 4. 퀴즈 풀기
    # ------------------------------------------------------------------
    def play_quiz(self):
        # 퀴즈가 하나도 없으면 안내하고 메뉴로 복귀
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(THIN_LINE)
            quiz.display(number)
            user_answer = self.read_int("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        # 점수 계산: 100점 만점으로 환산
        score = round(correct / total * 100)

        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        # 최고 점수 비교/갱신
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

        self.save_state()   # 점수가 바뀌었을 수 있으니 저장

    # ------------------------------------------------------------------
    # 5. 퀴즈 추가
    # ------------------------------------------------------------------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = self.read_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):                      # 선택지 4개
            choices.append(self.read_text(f"선택지 {i}: "))

        answer = self.read_int("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()                          # 추가한 퀴즈를 파일에 저장
        print("\n✅ 퀴즈가 추가되었습니다!")

    # ------------------------------------------------------------------
    # 6. 퀴즈 목록
    # ------------------------------------------------------------------
    def list_quizzes(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    # ------------------------------------------------------------------
    # 7. 점수 확인
    # ------------------------------------------------------------------
    def show_score(self):
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

    # ------------------------------------------------------------------
    # 8. 파일 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------------
    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            # Quiz 객체는 JSON에 바로 못 쓰므로 딕셔너리로 바꿔서 저장
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                # ensure_ascii=False: 한글이 \uXXXX 가 아니라 그대로 저장됨
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {e}")

    def load_state(self):
        """state.json을 읽어 온다. 없거나 망가졌으면 기본 퀴즈로 시작한다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 읽은 딕셔너리들을 Quiz 객체로 복원 (이상하면 오류 발생)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data["best_score"]
            if best_score is not None and (not isinstance(best_score, int)
                                           or not 0 <= best_score <= 100):
                raise ValueError("best_score 값이 올바르지 않습니다.")

        except FileNotFoundError:
            # 첫 실행: 파일이 없는 건 정상 상황
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            print("📂 저장 파일이 없어 기본 퀴즈로 시작합니다.")
            self.save_state()

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            # 파일이 손상됨 (JSON 형식 오류, 키 없음, 값 이상 등)
            print("⚠️ 저장 파일이 손상되어 기본 데이터로 초기화합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.save_state()

        except OSError as e:
            # 권한 문제 등 읽기 자체가 실패
            print(f"⚠️ 저장 파일을 읽지 못했습니다({e}). 기본 데이터로 시작합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None

        else:
            # 오류 없이 끝났을 때만 실행: 정상 불러오기
            self.quizzes = quizzes
            self.best_score = best_score
            score_text = "기록 없음" if best_score is None else f"{best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. "
                  f"(퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

    # ------------------------------------------------------------------
    # 9. 메인 루프
    # ------------------------------------------------------------------
    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.read_int("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                else:                      # 5: 종료
                    print("\n👋 게임을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료: 오류 화면 대신 안내 메시지
            print("\n\n⚠️ 입력이 중단되어 안전하게 종료합니다.")

        finally:
            # 정상 종료든 Ctrl+C든 마지막에 항상 저장
            self.save_state()