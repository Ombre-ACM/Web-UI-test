import unittest
from ddt import ddt, data, unpack, file_data
from web_keys.keys import Key


@ddt
class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = Key('Chrome')
        cls.url = 'http://www.guazi.com'

    @classmethod
    def tearDownClass(cls) -> None:
        cls.key.quit()

    # 主页搜索测试
    @data('不存在的车', '丰田', '福特')
    def test_001_search(self, txt):
        self.key.open(self.url)
        self.key.click('xpath', '//div[@class="wx-bar__close"]')
        self.key.input('name', 'keyword', txt)
        self.key.click('xpath', '//button[text()="搜索"]')
        self.key.assert_text('xpath', '//span[@class="tag"]', txt)
        result = self.key.locate('xpath', '//span[@class="tag"]').text
        self.assertEqual(result, txt, '断言失败')
        self.key.sleep(2)

    # 跳转城市测试
    @file_data('../data/change_city.yaml')
    def test_002_change_city(self, **kwargs):
        self.key.open(self.url)
        self.key.mouse_stop_at(**kwargs['stop_at'])
        self.key.click(**kwargs['click'])
        self.key.assert_text(**kwargs['assert_text'])
        result = self.key.locate(**kwargs['result']).text
        self.assertEqual(result, kwargs['assert_equal'], '断言失败')
        self.key.sleep(2)

    # 品牌直达链接测试
    @data('本田', '宝马', '奔驰')
    def test_003_brand_click(self, brand):
        self.key.open(self.url)
        self.key.click('xpath', '//span[text()="{}"]'.format(brand))
        self.key.assert_text('xpath', '//span[@class="tag"]', "{}".format(brand))
        result = self.key.locate('xpath', '//span[@class="tag"]').text
        self.assertEqual(result, "{}".format(brand), '断言失败')
        self.key.sleep(2)

    # 价格区间筛选测试
    @unittest.skip('价格进行了加密，暂无法获取')
    @file_data('../data/price_item.yaml')  # 这里网站对价格进行了加密 跳过
    def test_004_price_click(self, **kwargs):
        self.key.open(self.url)
        self.key.click('xpath', kwargs['price_item'])
        result = self.key.locate('xpath', '//span[@class="price-now"]/span[1]').text
        print(result)

    # 我要买车页面测试
    @file_data('../data/buy.yaml')
    def test_005_buy(self, **kwargs):
        self.key.open(self.url)
        self.key.click('xpath', '//*[text()="我要买车"]')
        self.key.click(**kwargs['brand'])
        self.key.click(**kwargs['series'])

        self.key.mouse_stop_at(**kwargs['stop_at_age'])
        self.key.click(**kwargs['age'])

        self.key.mouse_stop_at(**kwargs['stop_at_miles'])
        self.key.click(**kwargs['miles'])

        self.key.mouse_stop_at(**kwargs['stop_at_liter'])
        self.key.click(**kwargs['liter'])

        self.key.mouse_stop_at(**kwargs['stop_at_shift'])
        self.key.click(**kwargs['shift'])

        self.key.mouse_stop_at(**kwargs['stop_at_type'])
        self.key.click(**kwargs['type'])

        self.key.sleep(3)

        # 我要卖车页面测试
    def test_006_sell(self):
        self.key.open(self.url)
        self.key.click('xpath', '//*[text()="我要卖车"]')
        self.key.switch_handle(close=True, index=1)
        self.key.input('xpath', '//input[@class="phone-input js-phone-input"]', 15757828888)
        self.key.sleep(2)
        self.key.click('xpath', '//i[@class="icon-checkbox--gray"]')
        self.key.click('xpath', '//button[@class="phone-btn-1 free-sell-btn"]')
        # 车型信息
        self.key.click('xpath', '//img[@class="brand-selection__hot-item__image"]')
        self.key.click('xpath', '//div[@class="brand-selection__type-selection__list-item"]')
        self.key.click('xpath', '//div[@class="brand-selection__model-selection__list-item"]')
        self.key.sleep(1)
        # 车况信息
        self.key.input('xpath', '//input[@placeholder="请输入行驶里程"]', '1')
        self.key.click('xpath', '//div[@class="car-condition__item__date__label"]')
        self.key.click('xpath', '//div[@class="car-condition__item__date__year"]')
        self.key.click('xpath', '//div[@class="car-condition__item__date__month car-condition__item__date--right"]')
        self.key.sleep(1)

        # self.key.input('xpath', '//input[@class="appoint-info__location__collector"]', '宁波市')
        # self.key.click('xpath', '//*[@id="amap-sug0"]')
        self.key.click('xpath', '//i[@class="appoint-info__time__time-item__checkbox--default"]')
        # 点击预约，这里不进行操作
        # self.key.click('xpath', '//div[@class="direct-submit"]')

        self.key.sleep(3)

    # 瓜子金融
    def test_007_finance(self):
        self.key.open(self.url)
        self.key.click('xpath', '//*[text()="瓜子金融"]')
        self.key.switch_handle(close=True, index=1)
        self.key.sleep(3)

    # 毛豆新车
    def test_008_new_car(self):
        self.key.open(self.url)
        self.key.click('xpath', '//*[text()="毛豆新车"]')
        self.key.switch_handle(close=True, index=1)
        self.key.sleep(3)

    # 热卖
    @file_data('../data/hot_sell.yaml')
    def test_009_hot_sell(self, **kwargs):
        self.key.open(self.url)
        # self.key.move_to('xpath', '//h5[text()="热卖车型"]')
        # self.key.driver.execute_script('window.scrollBy(0,700)')
        self.key.mouse_stop_at('xpath', kwargs['value'])
        self.key.sleep(1)

    # 车辆详情页及导流
    def test_010_car_information(self):
        self.key.open(self.url)
        self.key.click('xpath', '//img[@class="card-pic"]')
        self.key.sleep(1)
        self.key.switch_handle(close=True, index=1)
        self.key.click('xpath', '//a[@class="greenbtn js-bargain"]')
        print("导流到APP进行成交")
        self.key.sleep(3)


if __name__ == '__main__':
    unittest.main()
