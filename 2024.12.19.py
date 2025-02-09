import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
current_window = driver.current_window_handle
url = 'https://flight.naver.com/'
driver.get(url)

#set up screen size
driver.maximize_window()


# select destination
def find_and_click(driver, status, city):
    destination = driver.find_element(By.XPATH,
                                       f'//button[contains(@class, "tabContent_route__EXyDz select_City__mKbzk") and contains(@class, "{status}")]')
    destination.click()
    time.sleep(2)

    input_field = driver.find_element(By.XPATH, '//input[@class ="autocomplete_input__qbYlb"]')
    input_field.send_keys(city)
    time.sleep(2)

    input_click = driver.find_element(By.XPATH, '//i[@class="searchResults_icon__JUOVX"]')
    input_click.click()
    time.sleep(2)

def search_flights(driver, dep, arr):
    find_and_click(driver,"start", dep)
    find_and_click(driver,"end", arr )

    calendar = driver.find_element(By.XPATH, "//button[contains(@class,'tabContent_option___mYJO select_Date__Potbp')]")
    calendar.click()
    time.sleep(1)

# select time
def select_time(date_str):
    year, month, day = date_str.split(".")
    year_month = f"{year}.{month}."
    date = str(int(day))
    return year_month, date


def year_month_date(driver, year_month_target, date_target):
    year_months = driver.find_elements(By.XPATH, "//div[contains(@class,'month')]")
    for year_month in year_months:
        year_month_text = year_month.text.strip().split("\n")[0]
        if year_month_text == year_month_target:
            driver.execute_script("arguments[0].scrollIntoView();", year_month)
            print(f"{year_month_target} is selected")
            time.sleep(2)

            days = year_month.find_elements(By.XPATH, ".//b[@class ='sc-cwHptR hFwLsU num']")
            for day in days:
                day_text = day.text.strip()
                if day_text == date_target:
                    day.click()
                    print(f"{date_target} is selected")
                    return
            print(f"{day_text} is not selected")
            break

if __name__ == "__main__":
    dep = input("Nhập điểm đi: ")
    arr = input("Nhập điểm đến: ")
    search_flights(driver, dep, arr)

    dep_time = input("Nhập ngày đi: ")
    arr_time = input("Nhập ngày đến: ")
    dep_year_month, dep_date = select_time(dep_time)
    arr_year_month, arr_date = select_time(arr_time)

    year_month_date(driver, dep_year_month, dep_date)
    year_month_date(driver, arr_year_month, arr_date)
    time.sleep(1)

# select seating
# select_seating_type = input ("일반석 = 1, 프리미엄 일반석 = 2, 비즈니스석 =3, 일등석 = 4. Input number :  ")
# list = ('일반석','프리미엄 일반석','비즈니스석','일등석')
# n = int(select_seating_type)
# seating = (list[n-1])
# num_people = driver.find_element(By.XPATH,'.//button[(contains(@class, "tabContent_option___mYJO select_Passenger__he8G8"))]')
# num_people.click()
# time.sleep(3)
# seats = driver.find_elements(By.XPATH,'.//button[(contains(@class, "searchBox_option__CxlUZ searchBox_as_seat__ntTOz"))]')
# for seat in seats:
#     if seat.text == seating:
#         seat.click()
#         time.sleep(2)
#         print (f" your seat is {seating} ")
#         break
# else:
#     print("we can't find this kind of seat")

# # Direct flight or not
# # aaa = input(" direct flight ? (y/n): ")
# # if aaa == "y":
# #     print("You have selected a direct flight")
# # else:
# #     print(" You have selected a non- direct flight ")
# # time.sleep(1)
# # neutral_area = driver.find_element(By.XPATH, './/div[@role = "tablist"]')
# # neutral_area.click()
# # time.sleep(1)
# # if aaa == "y":
# #     direct = driver.find_element(By.XPATH,
# #                              './/button[(contains(@class, "tabContent_option___mYJO tabContent_as_direct__dOk9T select_Direct__VsxJp"))]')
# #     direct.click()
# # time.sleep(1)
# submit_request
submit = driver.find_element(By.XPATH,'.//button[@type = "submit"]')
submit.click()
#
# #ticketflight
all_windows = driver.window_handles
for window in all_windows:
    if window != current_window:
        driver.switch_to.window(window)
        break

time.sleep(10)
#
prices = driver.find_elements(By.XPATH,'.//div[@class = "item_ItemPriceList__pAvJJ"]')
for price in prices:
    price_value = price.text
    time.sleep(10)
    match  = re.search(r'\d{1,3}(,\d{3})*(?=원)', price_value)
    if match:
        extracted_price = match.group().replace(",", "")
        #numeric_price = int(extracted_price)
        if int(extracted_price) <= 1300000:
            print(f"Extracted numeric price: {extracted_price}")
            actions = ActionChains(driver)
            actions.click(price).perform()
            select = driver.find_element(By.XPATH, './/div[@class = "item_item__uLNu7" ]')
            select.click()
            time.sleep(3)
            ticket = driver.find_element(By.XPATH, './/button[@class = "detail_button_expand__WMy7h"]')
            ticket.click()
            time.sleep(5)
            break



time.sleep(5)

while True:
    print("quit or not: \n")
    user_input = input("").strip().lower()
    if user_input == "quit":
        driver.quit()
        break



