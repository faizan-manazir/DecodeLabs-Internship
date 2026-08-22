"""Modern animated GUI for the DecodeLabs Password Security Analyzer."""
import customtkinter as ctk

from password_analyzer import analyze_password, load_common_passwords
from guess_time_estimator import estimate_guess_times


APP_TITLE = "Password Security Analyzer"


# ── Palette ──────────────────────────────────────────────────────────────────

COLORS = {
    "Weak": "#ef4444",
    "Medium": "#f59e0b",
    "Strong": "#22c55e",
    "Very Strong": "#3b82f6",
}

COMP_COLORS = {
    "lowercase": "#6366f1",
    "uppercase": "#a78bfa",
    "digits": "#22d3ee",
    "symbols": "#f472b6",
}

BG_DARK = "#0f1117"
CARD_BG = "#1a1d27"
ACCENT = "#6366f1"
ACCENT_DIM = "#35386b"
TEXT_PRI = "#e2e8f0"
TEXT_SEC = "#94a3b8"
DIVIDER = "#2d3148"


CHECK_LABELS = [
    ("length_ok", "Good password length (8+ characters)"),
    ("uppercase", "Contains uppercase letters"),
    ("lowercase", "Contains lowercase letters"),
    ("number", "Contains numbers"),
    ("special", "Contains special characters"),
]

RISK_LABELS = [
    ("common", "No common password detected"),
    ("repeated", "No repeated-character pattern"),
    ("sequential", "No obvious sequential pattern"),
    ("keyboard", "No keyboard-walk pattern"),
]


# ── Reusable helpers ─────────────────────────────────────────────────────────

def _ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


class SectionHeader(ctk.CTkFrame):
    """Icon + title header for a card section."""

    def __init__(self, master, icon: str, title: str, **kw):
        super().__init__(master, fg_color="transparent", **kw)

        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color=ACCENT,
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
            text_color=TEXT_SEC,
        ).grid(row=0, column=1, sticky="w")


class ScoreGauge(ctk.CTkFrame):
    """Canvas-drawn circular score gauge."""

    SIZE = 170
    LINE_W = 12
    START_ANGLE = 135
    SWEEP_FULL = 270

    def __init__(self, master, **kw):
        super().__init__(master, fg_color="transparent", **kw)

        self._canvas = ctk.CTkCanvas(
            self,
            width=self.SIZE,
            height=self.SIZE,
            bg=CARD_BG,
            highlightthickness=0,
        )

        self._canvas.pack()

        self._render_gauge(0, ACCENT_DIM)

    def _render_gauge(self, fraction: float, color: str):
        c = self._canvas
        c.delete("all")

        pad = self.LINE_W + 6
        bbox = (
            pad,
            pad,
            self.SIZE - pad,
            self.SIZE - pad,
        )

        # Background arc
        c.create_arc(
            *bbox,
            start=self.START_ANGLE,
            extent=self.SWEEP_FULL,
            outline=DIVIDER,
            width=self.LINE_W,
            style="arc",
        )

        # Score arc
        sweep = self.SWEEP_FULL * fraction

        if sweep > 0.5:
            c.create_arc(
                *bbox,
                start=self.START_ANGLE,
                extent=sweep,
                outline=color,
                width=self.LINE_W,
                style="arc",
            )

        cx = self.SIZE / 2
        cy = self.SIZE / 2

        value = int(round(fraction * 100))

        c.create_text(
            cx,
            cy - 8,
            text=str(value),
            fill=color,
            font=("Segoe UI", 32, "bold"),
        )

        c.create_text(
            cx,
            cy + 22,
            text="/ 100",
            fill=TEXT_SEC,
            font=("Segoe UI", 11),
        )

    def set(self, fraction: float, color: str):
        fraction = max(0.0, min(1.0, fraction))
        self._render_gauge(fraction, color)


class StrengthBadge(ctk.CTkFrame):
    """Pill-shaped strength label."""

    def __init__(self, master, **kw):
        super().__init__(
            master,
            corner_radius=14,
            fg_color=ACCENT_DIM,
            **kw,
        )

        self._label = ctk.CTkLabel(
            self,
            text="WAITING",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
            text_color="#ffffff",
        )

        self._label.pack(padx=16, pady=5)

    def set(self, text: str, bg: str):
        self.configure(fg_color=bg)
        self._label.configure(text=text)


class CompositionBar(ctk.CTkFrame):
    """Stacked horizontal bar showing password character composition."""

    BAR_H = 22

    def __init__(self, master, **kw):
        super().__init__(master, fg_color="transparent", **kw)

        self._canvas = ctk.CTkCanvas(
            self,
            height=self.BAR_H + 24,
            bg=CARD_BG,
            highlightthickness=0,
        )

        self._canvas.pack(fill="x")

        self._legend_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self._legend_frame.pack(fill="x", pady=(4, 0))

        self._reset()

    def _reset(self):
        self._canvas.delete("all")

        for widget in self._legend_frame.winfo_children():
            widget.destroy()

    def set(self, password: str):
        self._reset()

        if not password:
            return

        c = self._canvas
        c.update_idletasks()

        total_w = c.winfo_width()

        if total_w < 50:
            total_w = 400

        total_characters = len(password)

        counts = {
            "lowercase": 0,
            "uppercase": 0,
            "digits": 0,
            "symbols": 0,
        }

        for char in password:
            if char.islower():
                counts["lowercase"] += 1
            elif char.isupper():
                counts["uppercase"] += 1
            elif char.isdigit():
                counts["digits"] += 1
            else:
                counts["symbols"] += 1

        x = 0

        for key in ("lowercase", "uppercase", "digits", "symbols"):
            count = counts[key]

            if count == 0:
                continue

            segment_width = max(
                4,
                int(total_w * count / total_characters),
            )

            c.create_rectangle(
                x,
                2,
                x + segment_width,
                2 + self.BAR_H,
                fill=COMP_COLORS[key],
                outline="",
            )

            x += segment_width

        labels = {
            "lowercase": "a-z",
            "uppercase": "A-Z",
            "digits": "0-9",
            "symbols": "!@#",
        }

        column = 0

        for key in ("lowercase", "uppercase", "digits", "symbols"):
            count = counts[key]

            if count == 0:
                continue

            dot = ctk.CTkFrame(
                self._legend_frame,
                width=10,
                height=10,
                corner_radius=5,
                fg_color=COMP_COLORS[key],
            )

            dot.grid(
                row=0,
                column=column,
                padx=(8 if column else 0, 3),
            )

            column += 1

            ctk.CTkLabel(
                self._legend_frame,
                text=f"{labels[key]} ({count})",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=11,
                ),
                text_color=TEXT_SEC,
            ).grid(row=0, column=column)

            column += 1


class CharCounter(ctk.CTkFrame):
    """Live character count badge."""

    def __init__(self, master, **kw):
        super().__init__(
            master,
            corner_radius=10,
            fg_color=DIVIDER,
            **kw,
        )

        self._label = ctk.CTkLabel(
            self,
            text="0",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold",
            ),
            text_color=TEXT_SEC,
        )

        self._label.pack(padx=10, pady=2)

    def set(self, length: int):
        if length == 0:
            color = TEXT_SEC
            bg = DIVIDER

        elif length < 8:
            color = "#ef4444"
            bg = "#3b1111"

        elif length < 12:
            color = "#f59e0b"
            bg = "#3b2e0f"

        else:
            color = "#22c55e"
            bg = "#0f3b1a"

        self.configure(fg_color=bg)

        self._label.configure(
            text=str(length),
            text_color=color,
        )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

class PasswordAnalyzerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=BG_DARK)
        self.title(APP_TITLE)
        self.geometry("960x860")
        self.minsize(800, 700)

        self.common_passwords = load_common_passwords()

        self.password_var = ctk.StringVar()

        self._anim_id = None
        self._cur_score = 0.0

        self._build_ui()

        self.password_var.trace_add(
            "write",
            self._on_password_change,
        )

    # ──────────────────────────────────────────────────────────────────────
    # LAYOUT
    # ──────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Header ───────────────────────────────────────────────────────

        header = ctk.CTkFrame(
            self,
            fg_color=CARD_BG,
            corner_radius=0,
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="🛡️  Password Security Analyzer",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=26,
                weight="bold",
            ),
            text_color=TEXT_PRI,
        ).grid(
            row=0,
            column=0,
            pady=(18, 2),
        )

        ctk.CTkLabel(
            header,
            text=(
                "Advanced local password risk assessment  •  "
                "passwords never leave your device"
            ),
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
            text_color=TEXT_SEC,
        ).grid(
            row=1,
            column=0,
            pady=(0, 16),
        )

        # ── Main scrollable content ──────────────────────────────────────

        body = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_DARK,
            corner_radius=0,
        )

        body.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # ── Input card ───────────────────────────────────────────────────

        inp = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        inp.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(14, 10),
        )

        inp.grid_columnconfigure(0, weight=1)

        inp_header = ctk.CTkFrame(
            inp,
            fg_color="transparent",
        )

        inp_header.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=20,
            pady=(16, 6),
        )

        inp_header.grid_columnconfigure(0, weight=1)

        SectionHeader(
            inp_header,
            "🔑",
            "ENTER A PASSWORD",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.char_counter = CharCounter(inp_header)

        self.char_counter.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.entry = ctk.CTkEntry(
            inp,
            textvariable=self.password_var,
            show="•",
            height=46,
            corner_radius=10,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=16,
            ),
            fg_color="#12141e",
            border_color=ACCENT_DIM,
            placeholder_text="Type or paste a password…",
        )

        self.entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 8),
            pady=(0, 16),
        )

        self.show_btn = ctk.CTkButton(
            inp,
            text="👁  Show",
            width=90,
            height=46,
            corner_radius=10,
            fg_color=ACCENT_DIM,
            hover_color=ACCENT,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            command=self._toggle_show,
        )

        self.show_btn.grid(
            row=1,
            column=1,
            padx=(0, 6),
            pady=(0, 16),
        )

        ctk.CTkButton(
            inp,
            text="✕  Clear",
            width=90,
            height=46,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#2a2d3d",
            border_width=1,
            border_color=DIVIDER,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            command=self._clear,
        ).grid(
            row=1,
            column=2,
            padx=(0, 20),
            pady=(0, 16),
        )

        # ── Score card ───────────────────────────────────────────────────

        score_card = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        score_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20, 8),
            pady=10,
        )

        SectionHeader(
            score_card,
            "📊",
            "SECURITY SCORE",
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 4),
        )

        self.gauge = ScoreGauge(score_card)

        self.gauge.pack(
            pady=(6, 6),
        )

        self.strength_badge = StrengthBadge(score_card)

        self.strength_badge.pack(
            pady=(0, 6),
        )

        self.entropy_label = ctk.CTkLabel(
            score_card,
            text="Entropy: — bits",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
            text_color=TEXT_SEC,
        )

        self.entropy_label.pack(
            pady=(0, 20),
        )

        # ── Guess-time card ──────────────────────────────────────────────

        guess_card = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        guess_card.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 20),
            pady=10,
        )

        SectionHeader(
            guess_card,
            "⏱️",
            "GUESS-TIME ESTIMATE",
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10),
        )

        ctk.CTkLabel(
            guess_card,
            text="Offline (high-speed)",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
            text_color=TEXT_SEC,
        ).pack(
            anchor="w",
            padx=20,
        )

        self.offline_label = ctk.CTkLabel(
            guess_card,
            text="—",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=26,
                weight="bold",
            ),
            text_color=TEXT_PRI,
        )

        self.offline_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 14),
        )

        ctk.CTkFrame(
            guess_card,
            height=1,
            fg_color=DIVIDER,
        ).pack(
            fill="x",
            padx=20,
            pady=4,
        )

        ctk.CTkLabel(
            guess_card,
            text="Online (rate-limited)",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
            text_color=TEXT_SEC,
        ).pack(
            anchor="w",
            padx=20,
            pady=(14, 0),
        )

        self.online_label = ctk.CTkLabel(
            guess_card,
            text="—",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=20,
                weight="bold",
            ),
            text_color=TEXT_PRI,
        )

        self.online_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 8),
        )

        ctk.CTkLabel(
            guess_card,
            text="Estimates vary with hashing, hardware and rate limits.",
            wraplength=340,
            justify="left",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
            ),
            text_color="#64748b",
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18),
        )

        # ── Character composition ────────────────────────────────────────

        comp_card = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        comp_card.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=10,
        )

        SectionHeader(
            comp_card,
            "📐",
            "CHARACTER COMPOSITION",
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8),
        )

        self.comp_bar = CompositionBar(comp_card)

        self.comp_bar.pack(
            fill="x",
            padx=20,
            pady=(0, 18),
        )

        # ── Password analysis ────────────────────────────────────────────

        checks_card = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        checks_card.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=10,
        )

        SectionHeader(
            checks_card,
            "🔍",
            "PASSWORD ANALYSIS",
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10),
        )

        grid = ctk.CTkFrame(
            checks_card,
            fg_color="transparent",
        )

        grid.pack(
            fill="x",
            padx=20,
            pady=(0, 6),
        )

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            grid,
            text="Character checks",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color=TEXT_SEC,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 4),
        )

        ctk.CTkLabel(
            grid,
            text="Risk patterns",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color=TEXT_SEC,
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(16, 0),
            pady=(0, 4),
        )

        self.check_rows = {}

        for i, (key, label) in enumerate(CHECK_LABELS):
            row = ctk.CTkLabel(
                grid,
                text=f"○  {label}",
                anchor="w",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                ),
                text_color=TEXT_SEC,
            )

            row.grid(
                row=i + 1,
                column=0,
                sticky="w",
                pady=3,
            )

            self.check_rows[key] = row

        for i, (key, label) in enumerate(RISK_LABELS):
            row = ctk.CTkLabel(
                grid,
                text=f"○  {label}",
                anchor="w",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                ),
                text_color=TEXT_SEC,
            )

            row.grid(
                row=i + 1,
                column=1,
                sticky="w",
                padx=(16, 0),
                pady=3,
            )

            self.check_rows[key] = row

        self.entropy_label2 = ctk.CTkLabel(
            checks_card,
            text="Estimated entropy: — bits  •  estimate only",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
            text_color=TEXT_SEC,
        )

        self.entropy_label2.pack(
            anchor="w",
            padx=20,
            pady=(6, 20),
        )

        # ── Recommendations ──────────────────────────────────────────────

        rec_card = ctk.CTkFrame(
            body,
            fg_color=CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=DIVIDER,
        )

        rec_card.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(10, 8),
        )

        SectionHeader(
            rec_card,
            "💡",
            "SECURITY RECOMMENDATIONS",
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10),
        )

        self.recommendations = ctk.CTkTextbox(
            rec_card,
            height=100,
            corner_radius=10,
            fg_color="#12141e",
            wrap="word",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
            text_color=TEXT_PRI,
        )

        self.recommendations.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        self.recommendations.configure(state="disabled")

        # ── Footer ───────────────────────────────────────────────────────

        ctk.CTkLabel(
            body,
            text=(
                "🔒  All analysis runs locally — "
                "nothing is transmitted or intentionally stored"
            ),
            font=ctk.CTkFont(
                family="Segoe UI",
                size=11,
            ),
            text_color="#4b5068",
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(4, 18),
        )

    # ══════════════════════════════════════════════════════════════════════
    # ANALYZER CALLBACKS
    # ══════════════════════════════════════════════════════════════════════

    def _toggle_show(self):
        shown = self.entry.cget("show") == ""

        if shown:
            self.entry.configure(show="•")
            self.show_btn.configure(text="👁  Show")
        else:
            self.entry.configure(show="")
            self.show_btn.configure(text="👁  Hide")

    def _on_password_change(self, *_):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None

        password = self.password_var.get()

        self.char_counter.set(len(password))

        self._analyze()

    def _analyze(self):
        password = self.password_var.get()

        if not password:
            self._reset()
            return

        result = analyze_password(
            password,
            self.common_passwords,
        )

        self._render(
            result,
            password,
        )

    def _render(self, result, password):
        score = result["score"]
        strength = result["strength"]
        color = COLORS.get(strength, ACCENT)

        # Animate score
        self._animate_score(
            score,
            color,
        )

        # Strength badge
        self.strength_badge.set(
            strength.upper(),
            color,
        )

        # Entropy
        entropy = result["entropy_bits"]

        self.entropy_label.configure(
            text=f"Entropy: {entropy} bits"
        )

        self.entropy_label2.configure(
            text=f"Estimated entropy: {entropy} bits  •  estimate only"
        )

        # Guess-time estimation
        times = estimate_guess_times(
            entropy,
            result["risk_flags"],
        )

        self.offline_label.configure(
            text=times["offline"],
            text_color=color,
        )

        self.online_label.configure(
            text=times["online"],
        )

        # Character composition
        self.comp_bar.set(password)

        # Character checks
        for key, label in CHECK_LABELS:
            self._set_row(
                key,
                label,
                result["checks"][key],
            )

        # Risk checks
        for key, label in RISK_LABELS:
            self._set_row(
                key,
                label,
                not result["risk_flags"][key],
            )

        # Recommendations
        self.recommendations.configure(state="normal")
        self.recommendations.delete("1.0", "end")

        recommendations = result.get("recommendations", [])

        if recommendations:
            text = "\n".join(
                f"•  {item}"
                for item in recommendations
            )
        else:
            text = (
                "•  Good password characteristics detected. "
                "Continue using a unique password that is not reused "
                "across multiple accounts."
            )

        self.recommendations.insert(
            "end",
            text,
        )

        self.recommendations.configure(state="disabled")

    def _animate_score(self, target: int, color: str):
        start = self._cur_score
        steps = 24
        delay_ms = 14

        def tick(i=0):
            progress = min(i / steps, 1.0)

            value = start + (
                target - start
            ) * _ease_out_cubic(progress)

            self._cur_score = value

            self.gauge.set(
                value / 100,
                color,
            )

            if i < steps:
                self._anim_id = self.after(
                    delay_ms,
                    lambda: tick(i + 1),
                )
            else:
                self._anim_id = None

        tick()

    def _set_row(self, key, label, passed):
        if passed:
            symbol = "✓"
            color = "#22c55e"
        else:
            symbol = "✗"
            color = "#ef4444"

        self.check_rows[key].configure(
            text=f"{symbol}  {label}",
            text_color=color,
        )

    def _clear(self):
        self.password_var.set("")

    def _reset(self):
        self._cur_score = 0.0

        self.gauge.set(
            0,
            ACCENT_DIM,
        )

        self.strength_badge.set(
            "WAITING",
            ACCENT_DIM,
        )

        self.entropy_label.configure(
            text="Entropy: — bits"
        )

        self.entropy_label2.configure(
            text="Estimated entropy: — bits  •  estimate only"
        )

        self.offline_label.configure(
            text="—",
            text_color=TEXT_PRI,
        )

        self.online_label.configure(
            text="—",
        )

        self.comp_bar.set("")

        self.char_counter.set(0)

        for key, label in CHECK_LABELS + RISK_LABELS:
            self.check_rows[key].configure(
                text=f"○  {label}",
                text_color=TEXT_SEC,
            )

        self.recommendations.configure(state="normal")
        self.recommendations.delete("1.0", "end")
        self.recommendations.configure(state="disabled")


if __name__ == "__main__":
    PasswordAnalyzerApp().mainloop()
