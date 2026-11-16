from pathlib import Path
from app.database import engine


def popular():
    seed_path = Path(__file__).resolve().parent / "seed.sql"

    with open(seed_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conexao = engine.raw_connection()
    try:
        cursor = conexao.cursor()
        cursor.executescript(sql_script)
        conexao.commit()
        print("Banco povoado com sucesso!")
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao povoar o banco: {e}")
    finally:
        conexao.close()


if __name__ == "__main__":
    popular()
