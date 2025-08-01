"""Initial Migration

Revision ID: e6ea7e1c515d
Revises: 
Create Date: 2025-06-15 21:02:05.296154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6ea7e1c515d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('semester_id', sa.Integer(), nullable=True),
    sa.Column('ammount_pay', sa.Integer(), nullable=True),
    sa.Column('mode_of_payment', sa.Enum('Online', 'Cash'), nullable=True),
    sa.Column('pay_id', sa.String(length=100), nullable=True),
    sa.Column('order_id', sa.String(length=200), nullable=True),
    sa.Column('signature', sa.String(length=200), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['semester_id'], ['semester.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('payment_id')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), nullable=False),
    sa.Column('dept_id', sa.Integer(), nullable=False),
    sa.Column('sem_id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['dept_id'], ['department.dept_id'], ),
    sa.ForeignKeyConstraint(['sem_id'], ['semester.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['staffs.staff_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('enroll_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['enroll_id'], ['enrollment.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'enroll_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_table')
    op.drop_table('schedule')
    op.drop_table('payment')
    # ### end Alembic commands ###
