#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from typing import List, Tuple

# import pathlib
import flet as ft

DESKTOP = True
DATE_FORMAT = "%d/%m/%Y"
WEEK_DAYS = ("Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab")
MONTHS = (
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
    "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
)

calendar.setfirstweekday(calendar.SUNDAY)

global dia_final

def main(page: ft.Page):    

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.close()
        elif e.key in ("Enter", "Return", "Numpad Enter"):
            button_calcular_clicked(e)
            tf_months.focus()
            page.update()

    def get_grid_month_datatable(
            list_mount: List, par_month: int, par_year: int
    ) -> ft.DataTable:
        grip_datatable = ft.DataTable(
            bgcolor="gray",
            # border=ft.border.all(2, "black"),
            border_radius=10,
            divider_thickness=0,
            column_spacing=14,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=26,
            data_row_min_height=22,
            columns=[
                ft.DataColumn(
                    ft.Container(
                        content=ft.Text(
                            day_week,
                            style=ft.TextThemeStyle.TITLE_LARGE,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    numeric=True,
                ) for day_week in WEEK_DAYS
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row(
                                [
                                    get_menu(
                                        day_month=day, day_week=day_week,
                                        year=par_year, par_month=par_month
                                    ) if day else ft.Text(''),
                                ],
                            ),
                        ) for day_week, day in enumerate(week)
                    ],
                ) for week in list_mount
            ],
        )
        return grip_datatable

    def get_menu(
            day_month: int = 0,
            day_week: int = 0,
            year: int = 0,
            par_month: int = 0
    ) -> ft.PopupMenuButton:
        style = ft.TextThemeStyle.TITLE_LARGE
        text_align = ft.TextAlign.CENTER
        color = ft.colors.RED if day_week in (0, 6) else ft.colors.BLUE        
        day_now = f"{year}-{par_month:02}-{day_month:02}"
        # print(f"-> {dia_final}={day_now}")
        if day_now == dia_final:
            color = ft.colors.GREEN
            style = ft.TextThemeStyle.DISPLAY_MEDIUM
            text_align = ft.TextAlign.LEFT
        pm_button = ft.PopupMenuButton(
            content=ft.Text(
                str(day_month),
                style=style,
                color=color,
                text_align=text_align,
            ),
            items=[]
        )
        return pm_button

    def holidays_update_calendar(_final_date: datetime) -> None:
        for control in page.controls:
            if isinstance(control, ft.GridView):
                # print(f'Removendo calendário {_final_date} de {control.uid}')
                page.controls.remove(control)

        calendars = ft.GridView(
            runs_count=3,
            max_extent=450,
            child_aspect_ratio=0.999,
            spacing=16,
            run_spacing=16,
            expand=True,
        )

        # print(f'start day: {_final_date}')
        month_range: Tuple = (
            _final_date.month - 1,
            _final_date.month + 2,
        )
        # print(f"meses: {month_range}")

        for index_month in range(*month_range):
            cal_month = index_month if index_month > 0 else 12 + index_month
            cal_year = _final_date.year if index_month > 0 else _final_date.year - 1
            if cal_month > 12:
                cal_month = cal_month - 12
                cal_year = cal_year + 1
            # print(
            #     (
            #         f"{index_month} <> {cal_month}, {cal_year}"
            #         f" <> {cal_year}"
            #     )
            # )
            calendars.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        f"{MONTHS[cal_month - 1]} {cal_year}",
                                        text_align=ft.TextAlign.CENTER,
                                        style=ft.TextThemeStyle.TITLE_LARGE,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Container(
                                content=get_grid_month_datatable(
                                    calendar.monthcalendar(cal_year, cal_month),
                                    cal_month, cal_year,
                                ),
                                alignment=ft.alignment.center,
                            ),
                        ],
                    ),
                    bgcolor=ft.colors.AMBER_100,
                    alignment=ft.alignment.center,
                    padding=5,
                    border_radius=10,
                )
            )
        page.add(calendars)
        page.update()

    page.title = "Calculadora de Meses"
    icon_image = ft.Image(
        src="/images/schedule.png",
        width=128,
        height=128,
        fit=ft.ImageFit.SCALE_DOWN,
    )

    def button_calcular_clicked(e):
        global dia_final

        if e:
            pass
        
        try:
            end_date = datetime.datetime.strptime(tf_start_date.value, "%d%m%Y")
        except ValueError:
            try:
                end_date = datetime.datetime.strptime(tf_start_date.value, DATE_FORMAT)
            except ValueError:
                try:
                    end_date = datetime.datetime.strptime(tf_start_date.value, "%Y-%m-%d")
                except ValueError:
                    end_date = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
        tf_start_date.value = end_date.strftime(DATE_FORMAT)
            
        end_date_months = end_date + relativedelta(months=int(tf_months.value))
        dia_final = end_date_months.strftime("%Y-%m-%d")

        text_result = (
            f"Data final após {tf_months.value} meses: "
            f"{end_date_months.strftime(DATE_FORMAT)}"
        )
        txt_work_days_result.value = text_result

        holidays_update_calendar(end_date_months)
        page.update()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 10
    page.auto_scroll = True
    page.on_keyboard_event = on_keyboard

    final_date = datetime.datetime.today()

    txt_work_days_result = ft.Text(
        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        color=ft.colors.INDIGO_900,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
    )
    
    tf_start_date = ft.TextField(
        label="Data Inicial de pagamento",
        icon=ft.icons.CALENDAR_MONTH,
        value=final_date.strftime(DATE_FORMAT),
        width=200,
    )

    tf_months = ft.TextField(
        label="Meses",
        icon=ft.icons.CALENDAR_TODAY,
        value='1',
        width=120,
    )

    bt_calc = ft.ElevatedButton(
        text="Calcular",
        color=ft.colors.BACKGROUND,
        bgcolor=ft.colors.BLUE_ACCENT,
        on_click=button_calcular_clicked,
    )

    main_menu_1 = ft.Row(
        [
            icon_image,
            tf_start_date,
            tf_months,
        ],
        wrap=True,
    )

    main_menu_2 = ft.Row(
        [
            bt_calc,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    main_menu_3 = ft.Row(
        [
            ft.Text(''),
            txt_work_days_result,
        ],
        wrap=True,
    )

    page.add(
        ft.Container(
            content=main_menu_1,
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=main_menu_2,
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=main_menu_3,
            alignment=ft.alignment.center,
        )
    )
    
    button_calcular_clicked(None)
    tf_start_date.focus()
    page.update()


if DESKTOP:
    ft.app(target=main, assets_dir="assets",)
else:
    ft.app(
        target=main, port=8551,
        view=ft.WEB_BROWSER,
        assets_dir="assets",
    )
