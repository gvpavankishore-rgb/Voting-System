from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_input = request.form["user_id"]

        db = get_db()
        voter = db.execute(
            "SELECT * FROM voters WHERE voter_id=? OR aadhar=?",
            (user_input, user_input)
        ).fetchone()

        if voter:
            session["voter_id"] = voter["id"]
            return redirect("/details")
        else:
            return "Invalid ID ❌"

    return render_template("login.html")


# ---------------- DETAILS PAGE ----------------
@app.route("/details")
def details():
    voter_id = session.get("voter_id")

    if not voter_id:
        return redirect("/")

    db = get_db()
    voter = db.execute("SELECT * FROM voters WHERE id=?", (voter_id,)).fetchone()

    return render_template("details.html", voter=voter)


# ---------------- VOTE PAGE ----------------
@app.route("/vote")
def vote():
    voter_id = session.get("voter_id")

    if not voter_id:
        return redirect("/")

    db = get_db()
    parties = db.execute("SELECT * FROM parties").fetchall()

    return render_template("vote.html", parties=parties)


# ---------------- SELECT PARTY → FINGERPRINT PAGE ----------------
@app.route("/fingerprint/<int:party_id>")
def fingerprint(party_id):
    voter_id = session.get("voter_id")

    if not voter_id:
        return redirect("/")

    # store selected party
    session["party_id"] = party_id

    return render_template("fingerprint.html")


# ---------------- VERIFY FINGERPRINT ----------------
@app.route("/verify_fingerprint", methods=["POST"])
def verify_fingerprint():
    voter_id = session.get("voter_id")
    party_id = session.get("party_id")

    if not voter_id or not party_id:
        return redirect("/")

    db = get_db()

    user = db.execute("SELECT * FROM voters WHERE id=?", (voter_id,)).fetchone()

    if user["has_voted"] == 1:
        return "Already Voted ❌"

    # 🔴 Fake fingerprint (replace later)
    fingerprint_ok = True

    if not fingerprint_ok:
        return "Fingerprint Failed ❌"

    # save vote
    db.execute(
        "INSERT INTO votes (voter_id, party_id) VALUES (?, ?)",
        (voter_id, party_id)
    )

    db.execute(
        "UPDATE voters SET has_voted=1 WHERE id=?",
        (voter_id,)
    )

    db.commit()

    return redirect(f"/success/{party_id}")


# ---------------- SUCCESS ----------------
@app.route("/success/<int:party_id>")
def success(party_id):
    db = get_db()
    party = db.execute("SELECT * FROM parties WHERE id=?", (party_id,)).fetchone()
    return render_template("success.html", party=party)


# ================= ADMIN PANEL =================

@app.route("/admin", methods=["GET", "POST"])
def admin():
    db = get_db()

    if request.method == "POST":
        name = request.form["name"]
        voter_id = request.form["voter_id"]
        aadhar = request.form["aadhar"]

        db.execute(
            "INSERT INTO voters (name, voter_id, aadhar) VALUES (?, ?, ?)",
            (name, voter_id, aadhar)
        )
        db.commit()

    voters = db.execute("SELECT * FROM voters").fetchall()

    return render_template("admin.html", voters=voters)


@app.route("/delete_voter/<int:id>")
def delete_voter(id):
    db = get_db()
    db.execute("DELETE FROM voters WHERE id=?", (id,))
    db.commit()
    return redirect("/admin")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)