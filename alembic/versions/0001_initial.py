"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-11 23:59:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "criterio_alerta",
        sa.Column("id_criterio", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=100), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_criterio_alerta_id_criterio", "criterio_alerta", ["id_criterio"])

    op.create_table(
        "orientacion_no_clinica",
        sa.Column("id_orientacion", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=100), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_orientacion_no_clinica_id_orientacion", "orientacion_no_clinica", ["id_orientacion"])

    op.create_table(
        "perfil",
        sa.Column("id_perfil", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(length=150), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index("ix_perfil_id_perfil", "perfil", ["id_perfil"])

    op.create_table(
        "persona",
        sa.Column("id_persona", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("apellido", sa.String(length=50), nullable=False),
        sa.Column("correo", sa.String(length=100), nullable=False),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.UniqueConstraint("correo"),
    )
    op.create_index("ix_persona_id_persona", "persona", ["id_persona"])

    op.create_table(
        "tipo_persona",
        sa.Column("id_tipop", sa.Integer(), primary_key=True),
        sa.Column("nombretp", sa.String(length=100), nullable=True),
        sa.Column("descripciontp", sa.String(length=200), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_tipo_persona_id_tipop", "tipo_persona", ["id_tipop"])

    op.create_table(
        "hoja_vida",
        sa.Column("id_hoja", sa.Integer(), primary_key=True),
        sa.Column("id_persona", sa.Integer(), sa.ForeignKey("persona.id_persona"), nullable=True),
        sa.Column("fecha_registro", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
    )
    op.create_index("ix_hoja_vida_id_hoja", "hoja_vida", ["id_hoja"])

    op.create_table(
        "usuario",
        sa.Column("id_usuario", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("id_persona", sa.Integer(), sa.ForeignKey("persona.id_persona"), nullable=True),
        sa.Column("id_perfil", sa.Integer(), sa.ForeignKey("perfil.id_perfil"), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.UniqueConstraint("id_persona"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_usuario_id_usuario", "usuario", ["id_usuario"])

    op.create_table(
        "detalle_hoja_vida",
        sa.Column("id_detalle", sa.Integer(), primary_key=True),
        sa.Column("id_hoja", sa.Integer(), sa.ForeignKey("hoja_vida.id_hoja"), nullable=True),
        sa.Column("fecha", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("id_criterio", sa.Integer(), sa.ForeignKey("criterio_alerta.id_criterio"), nullable=True),
        sa.Column("id_orientacion", sa.Integer(), sa.ForeignKey("orientacion_no_clinica.id_orientacion"), nullable=True),
        sa.Column("id_tipop", sa.Integer(), sa.ForeignKey("tipo_persona.id_tipop"), nullable=True),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column("persona_registra", sa.Integer(), sa.ForeignKey("persona.id_persona"), nullable=True),
    )
    op.create_index("ix_detalle_hoja_vida_id_detalle", "detalle_hoja_vida", ["id_detalle"])


def downgrade() -> None:
    op.drop_index("ix_detalle_hoja_vida_id_detalle", table_name="detalle_hoja_vida")
    op.drop_table("detalle_hoja_vida")
    op.drop_index("ix_usuario_id_usuario", table_name="usuario")
    op.drop_table("usuario")
    op.drop_index("ix_hoja_vida_id_hoja", table_name="hoja_vida")
    op.drop_table("hoja_vida")
    op.drop_index("ix_tipo_persona_id_tipop", table_name="tipo_persona")
    op.drop_table("tipo_persona")
    op.drop_index("ix_persona_id_persona", table_name="persona")
    op.drop_table("persona")
    op.drop_index("ix_perfil_id_perfil", table_name="perfil")
    op.drop_table("perfil")
    op.drop_index("ix_orientacion_no_clinica_id_orientacion", table_name="orientacion_no_clinica")
    op.drop_table("orientacion_no_clinica")
    op.drop_index("ix_criterio_alerta_id_criterio", table_name="criterio_alerta")
    op.drop_table("criterio_alerta")
