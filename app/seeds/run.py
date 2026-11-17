from dotenv import load_dotenv

load_dotenv()  # carga .env antes de leer la configuración

import typer  # noqa: E402

from app.seeds.service import (run_all, run_categories, run_posts,  # noqa: E402
                               run_tags, run_users)

app = typer.Typer(help="Seeds CLI - Mar del Plata Futbolera")


@app.command("all")
def all_():
    """Carga usuarios, categorías, tags y posts de ejemplo."""
    run_all()
    typer.echo("Todos los seeds creados")


@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")


@app.command("categories")
def categories():
    run_categories()
    typer.echo("Categorías cargadas")


@app.command("tags")
def tags():
    run_tags()
    typer.echo("Tags cargados")


@app.command("posts")
def posts():
    """Carga posts (y antes sus dependencias: usuarios, categorías y tags)."""
    run_posts()
    typer.echo("Posts cargados")


if __name__ == "__main__":
    app()
