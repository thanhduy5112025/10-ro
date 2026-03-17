from collections import Counter

# ===================== PLAYER =====================
class Player:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.alive = True


# ===================== GAME =====================
class LifeCodeGame:
    def __init__(self, players):
        self.players = players
        self.current_index = 0
        self.turn = 1
        self.reports = []   # Lưu report để gửi người chơi

    # ---------- ĐÁNH GIÁ MẬT MÃ ----------
    def evaluate_guess(self, secret, guess):
        correct_position = sum(s == g for s, g in zip(secret, guess))

        secret_counter = Counter(secret)
        guess_counter = Counter(guess)

        correct_total = sum(
            min(secret_counter[d], guess_counter[d]) for d in secret_counter
        )

        correct_wrong_position = correct_total - correct_position
        return correct_position, correct_wrong_position

    # ---------- LẤY NGƯỜI CÒN SỐNG ----------
    def get_alive_indices(self):
        return [i for i, p in enumerate(self.players) if p.alive]

    # ---------- LẤY HAI NGƯỜI BÊN CẠNH ----------
    def get_neighbors(self, index):
        alive = self.get_alive_indices()
        pos = alive.index(index)

        left_index = alive[pos - 1]                  # trước
        right_index = alive[(pos + 1) % len(alive)]  # sau

        return left_index, right_index

    # ---------- MỘT LƯỢT ----------
    def next_turn(self):
        alive = self.get_alive_indices()
        if not alive:
            return False

        if self.current_index not in alive:
            self.current_index = alive[0]

        attacker = self.players[self.current_index]
        left_i, right_i = self.get_neighbors(self.current_index)

        print(f"\n🂱 TURN {self.turn}: {attacker.name}")
        print("Có thể đoán:")
        print(f"1️⃣ Trước : {self.players[left_i].name}")
        print(f"2️⃣ Sau   : {self.players[right_i].name}")

        choice = input("GM chọn mục tiêu (1 hoặc 2): ").strip()
        target_index = left_i if choice == "1" else right_i
        target = self.players[target_index]

        guess = input("GM nhập mật mã được đoán (10 chữ số): ").strip()

        cp, cwp = self.evaluate_guess(target.code, guess)

        # ---------- REPORT ----------
        report = (
            f"- {attacker.name} đoán {target.name} là {guess}, "
            f"{cp} đúng vị trí | {cwp} đúng số sai vị trí"
        )

        print("🩸", report)
        self.reports.append(report)

        # ---------- XỬ LÝ CHẾT ----------
        if cp == 10:
            target.alive = False
            death_report = f"☠️ {target.name} đã bị loại."
            print(death_report)
            self.reports.append(death_report)

        # ---------- CHUYỂN LƯỢT ----------
        alive = self.get_alive_indices()
        if alive:
            idx = alive.index(self.current_index)
            self.current_index = alive[(idx + 1) % len(alive)]

        self.turn += 1
        return True

    # ---------- KIỂM TRA KẾT THÚC ----------
    def check_end(self):
        alive_players = [p for p in self.players if p.alive]

        if len(alive_players) == 1:
            final = f"🏆 NGƯỜI CHIẾN THẮNG: {alive_players[0].name}"
            print(final)
            self.reports.append(final)
            return True

        if len(alive_players) == 0:
            final = "💀 TẤT CẢ NGƯỜI CHƠI ĐÃ BỊ LOẠI — KHÔNG AI THẮNG."
            print(final)
            self.reports.append(final)
            return True

        return False


# ===================== SETUP GAME =====================
players = [
    Player("Lại Trọng Hải Nam", "1052964738"),
    Player("Trần Thanh Phong", "0518892603"),
    Player("Le Barbeecue", "8306394173"),
    Player("Thụy Thảo", "9073146802"),
    Player("Hồ Mỹ Triêm", "4861362185"),
    Player("Nguyen Vu Duc Nhan", "0372901564"),
]

# players = [
#     Player("A", "0"),
#     Player("B", "00012345678"),
#     Player("C", "0123456781"),

# ]

game = LifeCodeGame(players)

# ===================== RUN GAME =====================
while True:
    game.next_turn()
    if game.check_end():
        break

# ===================== FINAL REPORT =====================
print("\n===== REPORT GỬI NGƯỜI CHƠI =====")
for r in game.reports:
    print(r)
