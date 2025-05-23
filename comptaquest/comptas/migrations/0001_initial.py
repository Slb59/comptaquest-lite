# Generated by Django 5.2.1 on 2025-05-21 15:27

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("utils", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TransferTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_transaction", models.DateTimeField(db_index=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("date_pointed", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("updatable", models.BooleanField(default=True)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("Expense", "expense"),
                            ("Income", "income"),
                            ("Transfer", "transfer"),
                            ("Outgoings", "outgoings"),
                        ],
                        db_index=True,
                        default="Expense",
                        max_length=15,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("deleted", "Deleted")],
                        db_index=True,
                        default="active",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CurrentAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="the account name", max_length=50)),
                ("pointed_date", models.DateTimeField(blank=True, help_text="The last pointed date", null=True)),
                (
                    "current_pointed_date",
                    models.DateTimeField(
                        blank=True, help_text="The account is to be pointed at this date, but not finished", null=True
                    ),
                ),
                (
                    "current_pointed_balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="The amount of the balance that is being to be pointed",
                        max_digits=8,
                    ),
                ),
                (
                    "current_balance",
                    models.DecimalField(
                        decimal_places=2, default=0, help_text="The last amount of balance pointed", max_digits=8
                    ),
                ),
                (
                    "average_interest",
                    models.DecimalField(
                        decimal_places=2, default=0, help_text="The average interest that is expected for", max_digits=8
                    ),
                ),
                (
                    "ledger_analysis",
                    models.BooleanField(default=True, help_text="If the account is include in the ledger analysis"),
                ),
                ("created_date", models.DateTimeField(blank=True, null=True)),
                (
                    "closed_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="After the closed date it is not possibile to add transaction or modify this account",
                        null=True,
                    ),
                ),
                (
                    "bank_name",
                    models.CharField(choices=[("CE", "CE"), ("CA", "CA"), ("GMF", "GMF")], default="CA", max_length=15),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("account_type", models.CharField(default="Current", editable=False, max_length=15)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_user_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExpenseOutgoings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("last_integrated_date", models.DateTimeField(blank=True, null=True)),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("Monthly", "monthly"),
                            ("Half-yearly", "half-yearly"),
                            ("Quaterly", "quaterly"),
                            ("Yearly", "yearly"),
                        ],
                        default="Monthly",
                        max_length=15,
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("outgoings_type", models.CharField(default="Expense", editable=False, max_length=15)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_account_outgoings",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_category_expenses",
                        to="utils.categorycodification",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_payment_expenses",
                        to="utils.paymentcodification",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="IncomeOutgoings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("last_integrated_date", models.DateTimeField(blank=True, null=True)),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("Monthly", "monthly"),
                            ("Half-yearly", "half-yearly"),
                            ("Quaterly", "quaterly"),
                            ("Yearly", "yearly"),
                        ],
                        default="Monthly",
                        max_length=15,
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("outgoings_type", models.CharField(default="Income", editable=False, max_length=15)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_account_outgoings",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_category_incomes",
                        to="utils.categorycodification",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "income_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_payment_incomes",
                        to="utils.incomecodification",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="InvestmentAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="the account name", max_length=50)),
                ("pointed_date", models.DateTimeField(blank=True, help_text="The last pointed date", null=True)),
                (
                    "current_pointed_date",
                    models.DateTimeField(
                        blank=True, help_text="The account is to be pointed at this date, but not finished", null=True
                    ),
                ),
                (
                    "current_pointed_balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="The amount of the balance that is being to be pointed",
                        max_digits=8,
                    ),
                ),
                (
                    "current_balance",
                    models.DecimalField(
                        decimal_places=2, default=0, help_text="The last amount of balance pointed", max_digits=8
                    ),
                ),
                (
                    "average_interest",
                    models.DecimalField(
                        decimal_places=2, default=0, help_text="The average interest that is expected for", max_digits=8
                    ),
                ),
                (
                    "ledger_analysis",
                    models.BooleanField(default=True, help_text="If the account is include in the ledger analysis"),
                ),
                ("created_date", models.DateTimeField(blank=True, null=True)),
                (
                    "closed_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="After the closed date it is not possibile to add transaction or modify this account",
                        null=True,
                    ),
                ),
                (
                    "bank_name",
                    models.CharField(choices=[("CE", "CE"), ("CA", "CA"), ("GMF", "GMF")], default="CA", max_length=15),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("account_type", models.CharField(default="Investment", editable=False, max_length=15)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_user_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FundHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_value", models.DateTimeField(blank=True, null=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("notes", models.CharField(blank=True, max_length=300)),
                (
                    "investment_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_fund_distribution_accounts",
                        to="comptas.investmentaccount",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FundDistribution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fund_name", models.CharField(max_length=50)),
                (
                    "prct",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                ("fund_type", models.CharField(max_length=50)),
                (
                    "investment_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_fund_distribution_accounts",
                        to="comptas.investmentaccount",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ledger",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(choices=[("Closed", "closed"), ("Open", "open")], default="Open", max_length=15),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_ledgers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IncomeTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_transaction", models.DateTimeField(db_index=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("date_pointed", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("updatable", models.BooleanField(default=True)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("Expense", "expense"),
                            ("Income", "income"),
                            ("Transfer", "transfer"),
                            ("Outgoings", "outgoings"),
                        ],
                        db_index=True,
                        default="Expense",
                        max_length=15,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("deleted", "Deleted")],
                        db_index=True,
                        default="active",
                        max_length=10,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_account_transactions",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_category_incomes",
                        to="utils.categorycodification",
                    ),
                ),
                (
                    "income_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_payment_incomes",
                        to="utils.incomecodification",
                    ),
                ),
                (
                    "ledger",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_ledger_transactions",
                        to="comptas.ledger",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExpenseTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_transaction", models.DateTimeField(db_index=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ("date_pointed", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("updatable", models.BooleanField(default=True)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("Expense", "expense"),
                            ("Income", "income"),
                            ("Transfer", "transfer"),
                            ("Outgoings", "outgoings"),
                        ],
                        db_index=True,
                        default="Expense",
                        max_length=15,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("deleted", "Deleted")],
                        db_index=True,
                        default="active",
                        max_length=10,
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_account_transactions",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_category_expenses",
                        to="utils.categorycodification",
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_payment_expenses",
                        to="utils.paymentcodification",
                    ),
                ),
                (
                    "ledger",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_ledger_transactions",
                        to="comptas.ledger",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TransferOutgoings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50)),
                ("last_integrated_date", models.DateTimeField(blank=True, null=True)),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("Monthly", "monthly"),
                            ("Half-yearly", "half-yearly"),
                            ("Quaterly", "quaterly"),
                            ("Yearly", "yearly"),
                        ],
                        default="Monthly",
                        max_length=15,
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(500)]
                    ),
                ),
                ("outgoings_type", models.CharField(default="Transfer", editable=False, max_length=15)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_account_outgoings",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_category_incomes",
                        to="utils.categorycodification",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "link_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_link_account_transfers",
                        to="comptas.currentaccount",
                    ),
                ),
                (
                    "link_transfer",
                    models.OneToOneField(
                        blank=True,
                        help_text="The link transfer of this transfer node.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_link_transfer",
                        to="comptas.transferoutgoings",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TransferOutgoingsTransaction",
            fields=[
                (
                    "transfertransaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="comptas.transfertransaction",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("comptas.transfertransaction", models.Model),
        ),
        migrations.AddField(
            model_name="transfertransaction",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_account_transactions",
                to="comptas.currentaccount",
            ),
        ),
        migrations.AddField(
            model_name="transfertransaction",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_category_incomes",
                to="utils.categorycodification",
            ),
        ),
        migrations.AddField(
            model_name="transfertransaction",
            name="ledger",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_ledger_transactions",
                to="comptas.ledger",
            ),
        ),
        migrations.AddField(
            model_name="transfertransaction",
            name="link_account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_link_account_transfers",
                to="comptas.currentaccount",
            ),
        ),
        migrations.AddField(
            model_name="transfertransaction",
            name="link_transfer",
            field=models.OneToOneField(
                blank=True,
                help_text="The link transfer of this transfer node.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_link_transfer",
                to="comptas.transfertransaction",
            ),
        ),
        migrations.CreateModel(
            name="ExpenseOutgoingsTransaction",
            fields=[
                (
                    "expensetransaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="comptas.expensetransaction",
                    ),
                ),
                (
                    "last_transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_last_transactions",
                        to="comptas.expenseoutgoingstransaction",
                    ),
                ),
                (
                    "outgoings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_outgoings_transactions",
                        to="comptas.expenseoutgoings",
                        verbose_name="Outgoings Expense",
                    ),
                ),
                (
                    "previous_transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_previous_transactions",
                        to="comptas.expenseoutgoingstransaction",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("comptas.expensetransaction", models.Model),
        ),
        migrations.CreateModel(
            name="IncomeOutgoingsTransaction",
            fields=[
                (
                    "incometransaction_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="comptas.incometransaction",
                    ),
                ),
                (
                    "last_transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_last_transactions",
                        to="comptas.incomeoutgoingstransaction",
                    ),
                ),
                (
                    "outgoings",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_outgoings_transactions",
                        to="comptas.incomeoutgoings",
                        verbose_name="Outgoings Income",
                    ),
                ),
                (
                    "previous_transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_previous_transactions",
                        to="comptas.incomeoutgoingstransaction",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("comptas.incometransaction", models.Model),
        ),
        migrations.AddIndex(
            model_name="incometransaction",
            index=models.Index(fields=["account", "transaction_type"], name="idx_income_account_type"),
        ),
        migrations.AddIndex(
            model_name="incometransaction",
            index=models.Index(fields=["date_transaction", "account"], name="idx_income_date_account"),
        ),
        migrations.AddIndex(
            model_name="incometransaction",
            index=models.Index(fields=["status"], name="idx_income_status"),
        ),
        migrations.AddIndex(
            model_name="expensetransaction",
            index=models.Index(fields=["account", "transaction_type"], name="idx_expense_account_type"),
        ),
        migrations.AddIndex(
            model_name="expensetransaction",
            index=models.Index(fields=["date_transaction", "account"], name="idx_expense_date_account"),
        ),
        migrations.AddIndex(
            model_name="expensetransaction",
            index=models.Index(fields=["status"], name="idx_expense_status"),
        ),
        migrations.AddField(
            model_name="transferoutgoingstransaction",
            name="last_transaction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_last_transactions",
                to="comptas.transferoutgoingstransaction",
            ),
        ),
        migrations.AddField(
            model_name="transferoutgoingstransaction",
            name="outgoings",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_outgoings_transactions",
                to="comptas.transferoutgoings",
                verbose_name="Outgoings Transfer",
            ),
        ),
        migrations.AddField(
            model_name="transferoutgoingstransaction",
            name="previous_transaction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_previous_transactions",
                to="comptas.transferoutgoingstransaction",
            ),
        ),
        migrations.AddIndex(
            model_name="transfertransaction",
            index=models.Index(fields=["account", "transaction_type"], name="idx_transfer_account_type"),
        ),
        migrations.AddIndex(
            model_name="transfertransaction",
            index=models.Index(fields=["date_transaction", "account"], name="idx_transfer_date_account"),
        ),
        migrations.AddIndex(
            model_name="transfertransaction",
            index=models.Index(fields=["status"], name="idx_transfer_status"),
        ),
    ]
