"""main.py - 프로그램 시작점

실행 방법: python main.py
게임의 실제 동작은 quiz_game.py의 QuizGame 클래스가 담당하고,
이 파일은 게임 객체를 만들어 실행시키는 역할만 한다.
"""

from quiz_game import QuizGame


def main():
    game = QuizGame()   # 객체를 만들면 state.json을 자동으로 불러온다
    game.run()          # 메뉴 루프 시작


# 이 파일을 직접 실행(python main.py)했을 때만 main()을 호출한다.
# (다른 파일에서 import 할 때는 실행되지 않는다)
if __name__ == "__main__":
    main()