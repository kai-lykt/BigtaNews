from django.db import models
from smedaily.common.models import TimeStampMixin


class BasicInfo(TimeStampMixin):
    """
    주식 종목 기본정보
    """
    DEFAULT_CURRENCY_ID = 1
    DEFAULT_MARKET_ID = 1

    code = models.CharField(max_length=7, unique=True, help_text='종목코드')
    name = models.CharField(max_length=20, help_text='종목명')
    market = models.ForeignKey(
        'common.Market'
        , on_delete=models.PROTECT
        , help_text='시장'
        , default=DEFAULT_MARKET_ID
    )
    currency = models.ForeignKey(
        'common.Currency'
        , on_delete=models.PROTECT
        , help_text='사용 통화'
        , default=DEFAULT_CURRENCY_ID
    )
    corp_code = models.CharField(max_length=9, blank=True, default=' ', help_text='DART 고유번호')
    is_recommend = models.BooleanField(default=False, help_text='추천 종목')
    is_favorite = models.BooleanField(default=False, help_text='인기 종목')

    class Meta:
        db_table = 'stocks_basic_info'
        indexes = [
            models.Index(fields=['name'], name='stocks_basic_info_name_idx')    # 주식 종목명 인덱스
        ]
        ordering = ('code',)


class DetailInfo(TimeStampMixin):
    """
    주식 종목 상세정보
    """
    code = models.ForeignKey(
        'BasicInfo'
        , related_name='details'
        , on_delete=models.PROTECT
        , to_field='code'
        , help_text='종목코드'
    )
    time = models.BigIntegerField(help_text='시간 (hhmm)')
    updown_signal = models.IntegerField(
        choices=models.IntegerChoices('SignalType', '상한 상승 보합 하한 하락').choices
        , help_text='대비부호'
    )
    updown_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='전일대비')
    current_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='현재가')
    open_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='시가')
    high_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='고가')
    low_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='저가')
    ask_quote = models.DecimalField(max_digits=19, decimal_places=2, help_text='매도호가')
    bid_quote = models.DecimalField(max_digits=19, decimal_places=2, help_text='매수호가')
    transaction_volume = models.BigIntegerField(help_text='거래량')
    transaction_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='거래대금')
    market_state = models.IntegerField(
        choices=models.IntegerChoices('MarketStateCode', '장전 동시호가 장중 빈값').choices
        , default=4
        , help_text='장구분. 1: 장전, 2: 동시호가, 3: 장중, 4: 빈값'
    )
    total_ask_quote_redundancy = models.BigIntegerField(help_text='총매도호가잔량')
    total_bid_quote_redundancy = models.BigIntegerField(help_text='총매수호가잔량')
    first_ask_quote_redundancy = models.BigIntegerField(help_text='최우선매도호가잔량')
    first_bid_quote_redundancy = models.BigIntegerField(help_text='최우선매수호가잔량')
    total_listing_volume = models.BigIntegerField(help_text='총상장주식수')
    foreigner_holding_ration = models.FloatField(help_text='회국인보유비율')
    previous_volume = models.BigIntegerField(help_text='전일거래량')
    previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='전일종가')
    volume_power = models.FloatField(help_text='체결강도')
    volume_type = models.IntegerField(
        choices=models.IntegerChoices('VolumeTypeCode', '매수체결 매도체결 빈값').choices
        , default=3
        , help_text='체결구분. 1: 매수체결, 2: 매도체결, 3: 빈값'
    )
    open_interest = models.BigIntegerField(help_text='미결제약정')
    expected_closing_price = models.BigIntegerField(help_text='예상체결가')
    expected_closing_updown = models.BigIntegerField(help_text='예상체결가대비')
    expected_closing_updown_signal = models.IntegerField(
        choices=models.IntegerChoices('SignalType', '상한 상승 보합 하한 하락 빈값').choices
        , help_text='예상체결가 대비부호'
    )
    expected_volume = models.BigIntegerField(help_text='예상체결수량')
    nineteen_closing_sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='19일 종가합')
    upper_limit = models.DecimalField(max_digits=19, decimal_places=2, help_text='상한가')
    lower_limit = models.DecimalField(max_digits=19, decimal_places=2, help_text='하한가')
    sales_quantity_unit = models.PositiveSmallIntegerField(help_text='매매수량단위')
    foreigner_net_sale_volume = models.BigIntegerField(help_text='외국인순매매. 단위: 주')
    fiftytwoweek_high_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='52주 최고가')
    fiftytwoweek_low_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='52주 최저가')
    year_high_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='연중 최고가')
    year_low_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='연중 최저가')
    price_earning_ratio = models.FloatField(help_text='PER')
    earning_per_share = models.BigIntegerField(help_text='EPS')
    capital = models.BigIntegerField(help_text='자본금. 단위: 백만')
    par_value = models.PositiveSmallIntegerField(help_text='액면가')
    allocation_ratio = models.FloatField(help_text='배당률')
    allocation_earning_ratio = models.FloatField(help_text='배당수익률')
    debt_ratio = models.FloatField(help_text='부채비율')
    reservation_ratio = models.FloatField(help_text='유보율')
    equity_capital_ratio = models.FloatField(help_text='자기자본이익률')
    sales_growth_ratio = models.FloatField(help_text='매출이익증가율')
    ordinary_profit_growth_ratio = models.FloatField(help_text='경상이익증가율')
    net_profit_growth_ratio = models.FloatField(help_text='순이익증가율')
    sentiment_indicators = models.FloatField(help_text='투자심리')
    volume_ratio = models.FloatField(help_text='VR')
    fiveday_turnover_ratio = models.FloatField(help_text='5일 회전율')
    fourday_closeprice_sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='4일 종가합')
    nineday_closeprice_sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='9일 종가합')
    revenue = models.BigIntegerField(help_text='매출액. 단위: 백만')
    ordinary_profit = models.BigIntegerField(help_text='경상이익. 단위: 원')
    net_profit = models.BigIntegerField(help_text='당기 순이익. 단위: 원')
    bookvalue_per_share = models.BigIntegerField(help_text='BPS 주당 순 자산')
    operating_income_growth_ratio = models.FloatField(help_text='영업이익증가율')
    operating_income = models.DecimalField(max_digits=19, decimal_places=2, help_text='영업이익')
    operating_income_to_sales_ratio = models.FloatField(help_text='매출액영업이익률')
    ordinary_profit_to_sales_ratio = models.FloatField(help_text='매출액경상이익률')
    interest_coverage_ratio = models.FloatField(help_text='이자보상비율')
    closing_account_date = models.PositiveIntegerField(help_text='결산년월 yyyyMM')
    quarter_bookvalue_per_share = models.BigIntegerField(help_text='분기BPS. 분기주당순자산')
    quarter_revenue_growth_ratio = models.FloatField(help_text='분기매출액증가율')
    quarter_operating_income_growth_ratio = models.FloatField(help_text='분기영업이익증가율')
    quarter_ordinary_profit_growth_ratio = models.FloatField(help_text='분기경상이익증가율')
    quarter_net_profit_growth_ratio = models.FloatField(help_text='분기순이익증가율')
    quarter_sales = models.DecimalField(max_digits=19, decimal_places=2, help_text='분기매출액. 단위: 백만')
    quarter_operating_income = models.DecimalField(max_digits=19, decimal_places=2, help_text='분기영업이익. 단위: 원')
    quarter_ordinary_profit = models.DecimalField(max_digits=19, decimal_places=2, help_text='분기경상이익. 단위: 원')
    quarter_net_profit = models.DecimalField(max_digits=19, decimal_places=2, help_text='분기당기순이익. 단위: 원')
    quarter_operating_income_to_sales_ratio = models.FloatField(help_text='분기매출액영업이익률')
    quarter_ordinary_profit_to_sales_ratio = models.FloatField(help_text='분기매출액경상이익률')
    quarter_return_on_equity = models.FloatField(help_text='분기 ROE. 자기자본순이익률')
    quarter_interest_coverage_ratio = models.FloatField(help_text='분기이자보상비율')
    quarter_reserve_ratio = models.FloatField(help_text='분기유보율')
    quarter_debr_ration = models.FloatField(help_text='분기부채비율')
    last_quarter_yyyymm = models.PositiveIntegerField(help_text='최근분기년월 yyyyMM')
    basis = models.FloatField(help_text='BASIS')
    local_date_yyyymmdd = models.PositiveIntegerField(help_text='현지날짜 yyyyMMdd')
    nation = models.TextField(help_text='해외지수국가명')
    elw_theoretical_value = models.DecimalField(max_digits=19, decimal_places=2, help_text='ELW 이론가')
    program_net_bid = models.BigIntegerField(help_text='프로그램 순 매수')
    today_foregier_net_bid_porvisional_yesno = models.IntegerField(
        choices=models.IntegerChoices('YesNoType', '해당없음 확정 잠정').choices
        , help_text='당일외국인순매수잠정구분'
    )
    today_foregier_net_bid = models.BigIntegerField(help_text='당일 외국인 순매수')
    today_institution_net_bid_porvisional_yesno = models.IntegerField(
        choices=models.IntegerChoices('YesNoType', '해당없음 확정 잠정').choices
        , help_text='당일기관순매수잠정구분'
    )
    today_institution_net_bid = models.BigIntegerField(help_text='당일 기관 순매수')
    previous_foregier_net_bid = models.BigIntegerField(help_text='전일 외국인 순매수')
    previous_institution_net_bid = models.BigIntegerField(help_text='전일 기관 순매수')
    sales_per_share = models.DecimalField(max_digits=19, decimal_places=2, help_text='SPS')
    cash_flow_per_share = models.DecimalField(max_digits=19, decimal_places=2, help_text='CFPS')
    earning_before_interest_tax_depreciation_amortization = models.DecimalField(
        max_digits=19, decimal_places=2, help_text='EVITDA'
    )
    credit_balance_ratio = models.FloatField(help_text='신용잔고율')
    short_selling_quantity = models.BigIntegerField(help_text='공매도수량')
    short_selling_date = models.BigIntegerField(help_text='공매도일자')
    index_futures_previous_unpaid_agreement = models.BigIntegerField(
        help_text='지수/주식선물 전일미결제약정'
    )
    beta = models.FloatField(help_text='베타계수')
    fiftynine_close_sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='59일 종가 합')
    oneonenine_close_sum = models.DecimalField(max_digits=19, decimal_places=2, help_text='119일 종가 합')
    today_retail_net_bid_porvisional_yesno = models.IntegerField(
        choices=models.IntegerChoices('YesNoType', '해당없음 확정 잠정').choices
        , help_text='당일 개인 순매수 잠정구분'
    )
    today_retail_net_bid = models.BigIntegerField(help_text='당일 개인 순매수')
    previous_retail_net_bid = models.BigIntegerField(help_text='전일 개인 순매수')
    five_previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='5일 전 종가')
    ten_previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='10일 전 종가')
    twenty_previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='20일 전 종가')
    sixty_previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='60일 전 종가')
    onehundredtwenty_previous_close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='120일 전 종가')
    estimated_static_vi_activation_base_price = models.DecimalField(
        max_digits=19, decimal_places=2, help_text='정적 VI 발동 예상 기준가'
    )
    estimated_static_vi_activation_rising_price = models.DecimalField(
        max_digits=19, decimal_places=2, help_text='정적 VI 발동 예상 상승가'
    )
    estimated_static_vi_activation_falling_price = models.DecimalField(
        max_digits=19, decimal_places=2, help_text='정적 VI 발동 예상 하락가'
    )
    data_date = models.DateField(auto_now_add=True, help_text='입력 날짜')

    class Meta:
        db_table = 'stocks_detail_info'
        unique_together = ['code', 'data_date']

    def __str__(self):
        return str(self.current_price)


class Parameter(TimeStampMixin):
    """
    주식 종목별 점수
    """
    code = models.ForeignKey(
        'BasicInfo'
        , related_name='parameters'
        , on_delete=models.PROTECT
        , to_field='code'
        , help_text='종목코드'
    )
    attractive = models.FloatField(help_text='배당 매력')
    growth = models.FloatField(help_text='성장성')
    stability = models.FloatField(help_text='재무 안정성')
    cash_generate = models.FloatField(help_text='현금 창출력')
    monopoly = models.FloatField(help_text='독점력')
    recommendation_value = models.IntegerField(help_text='추천 점수')
    data_date = models.DateField(auto_now_add=True, help_text='데이터 날짜')

    class Meta:
        db_table = 'stocks_parameter'
        unique_together = ['code', 'data_date']
        indexes = [
            models.Index(fields=['-data_date'], name='stocks_parameters_date_idx'),    # 날짜 인덱스
        ]


class HistoricData(TimeStampMixin):
    """HistoricData
    과거데이타
    """
    code = models.ForeignKey(
        'BasicInfo'
        , related_name='historic'
        , on_delete=models.PROTECT
        , to_field='code'
        , help_text='종목코드'
    )
    close = models.IntegerField
    close_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='종가')
    open_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='시가')
    high_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='고가')
    low_price = models.DecimalField(max_digits=19, decimal_places=2, help_text='저가')
    transaction_volume = models.BigIntegerField(help_text='거래량')
    date = models.DateField(help_text='날짜')

    class Meta:
        db_table = 'stocks_historic_data'
        unique_together = ['code', 'date']


class StocksSignal(TimeStampMixin):
    code = models.ForeignKey(
        'BasicInfo'
        , related_name='signals'
        , on_delete=models.PROTECT
        , to_field='code'
        , help_text='종목코드'
    )
    stock_name = models.CharField(max_length=300, help_text='종목명')
    signal = models.TextField(help_text='특이사항')
    date = models.DateField(help_text='날짜')
    time = models.CharField(max_length=10, help_text='시간')

    class Meta:
        db_table = 'stocks_signal'
        indexes = [
            models.Index(fields=['-date', '-time'], name='stocks_signal_date_time_idx'),    # 날짜 인덱스
        ]


class StockReports(TimeStampMixin):
    stock_name = models.CharField(max_length=20, help_text='종목명')
    stock_code = models.CharField(max_length=6, help_text='종목코드')
    title = models.CharField(max_length=100, help_text='제목')
    link = models.TextField(help_text='보고서 링크 url')
    fin_corp = models.CharField(max_length=20, help_text='증권사')
    date = models.DateField(help_text='작성일')

    class Meta:
        db_table = 'stocks_reports'
        indexes = [
            models.Index(fields=['stock_name'], name='stocks_reports_name'),
            models.Index(fields=['stock_code'], name='stocks_reports_code'),
        ]
