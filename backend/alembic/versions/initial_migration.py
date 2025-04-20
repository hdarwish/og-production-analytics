"""initial migration

Revision ID: initial
Revises: 
Create Date: 2024-02-20

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create wells table
    op.create_table(
        'well',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create production_data table
    op.create_table(
        'productiondata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('well_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('oil_volume', sa.Float(), nullable=True),
        sa.Column('gas_volume', sa.Float(), nullable=True),
        sa.Column('water_volume', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['well_id'], ['well.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_well_name'), 'well', ['name'], unique=False)
    op.create_index(op.f('ix_productiondata_date'), 'productiondata', ['date'], unique=False)
    op.create_index(op.f('ix_productiondata_well_id'), 'productiondata', ['well_id'], unique=False)

def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_productiondata_well_id'), table_name='productiondata')
    op.drop_index(op.f('ix_productiondata_date'), table_name='productiondata')
    op.drop_index(op.f('ix_well_name'), table_name='well')
    
    # Drop tables
    op.drop_table('productiondata')
    op.drop_table('well') 