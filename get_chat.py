from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc 

num = 2
chat_loading = True
before_text = ''

WEB_URL = "https://chat.openai.com/chat"

CHAT_ID = 'stackproton1@proton.me'
CHAT_PW = '@stackniki'

FULL_CAPACITY_XPATH = '//*[@id="__next"]/div[1]/div/div[1]/div[1]'

CLOUDFLARE_CHAKBOX_XPATH = '//*[@id="cf-stage"]/div[6]/label/input'

CHAT_LOGIN_XPATH = '//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]'

LOGIN_ID_XPATH = '//*[@id="username"]' 
LOGIN_PW_XPATH = '//*[@id="password"]'

CHAT_SEND_TEXT_XPATH = '//*[@id="__next"]/div[2]/div[1]/main/div[2]/form/div/div[2]/textarea'
CHAT_RESULT_STREAMING_CLASSNAME = 'result-streaming'

NEXT_BTN_1_XPATH = '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button'
NEXT_BTN_2_XPATH = '//*[@id="headlessui-dialog-panel-:r1:"]/div[2]/div[4]/button[2]'
DONE_BTN_CLASSNAME = 'btn-primary'

CHAT_NETWORK_ERROR = '//*[@id="__next"]/div[2]/div[1]/main/div[1]/div/div/div/div[8]/div/div[2]/div[1]/div/div'

ENTER = r'\n'

driver = uc.Chrome()

#driver.get("https://platform.openai.com/playground") 
driver.get(WEB_URL)

def cheak():
    print(driver.current_url)
    print(driver.title)

def is_max_capacity(text):
    print(text)
    if(text == None):
        return False
    else:
        return True
    
    #or something run code

def exist_element(by:list, element_info:list, event:list):
    by_len = len(by)

    while(1) :
        curr_len = None
        for i in range(by_len):
            try:
                element = driver.find_element(by[i], element_info[i])
                curr_len = i
            except:
                pass
    
        if(curr_len != None):
            break

    try:
        for i in event[curr_len]:
            eval(i)
    except:
        print(f"missing elements : [{element_info}]")

def chat_login():
    exist_element(by=[By.XPATH, By.XPATH, By.XPATH], element_info=[CHAT_LOGIN_XPATH, FULL_CAPACITY_XPATH, CLOUDFLARE_CHAKBOX_XPATH], 
                  event=[['element.click()'],
                         ['is_max_capacity(element.text)'],
                         ['login_pass_cloudflare(element)']]) 
    exist_element(by=[By.XPATH], element_info=[LOGIN_ID_XPATH], event=[[f'element.send_keys("{CHAT_ID}")', f'element.send_keys("{ENTER}")']])
    exist_element(by=[By.XPATH], element_info=[LOGIN_PW_XPATH], event=[[f'element.send_keys("{CHAT_PW}")', f'element.send_keys("{ENTER}")']])

    return

def pass_comment():
    exist_element(by=[By.XPATH], element_info=[NEXT_BTN_1_XPATH], event=[['element.click()']])
    exist_element(by=[By.XPATH], element_info=[NEXT_BTN_2_XPATH], event=[['element.click()']])
    exist_element(by=[By.CLASS_NAME], element_info=[DONE_BTN_CLASSNAME], event=[['element.click()']])
    return

def give_text(text:str):
    exist_element(by=[By.XPATH], element_info=[CHAT_SEND_TEXT_XPATH], event=[[f'element.send_keys("{text}")', f'element.send_keys("{ENTER}")']])
    
def is_loading(class_name=None):
    global chat_loading
    chat_loading = CHAT_RESULT_STREAMING_CLASSNAME in class_name
    return

def get_text():
    global num
    global chat_loading
    chat_loading = True

    CHAT_GET_TEXT_XPATH = f'//*[@id="__next"]/div[2]/div[1]/main/div[1]/div/div/div/div[{num}]/div/div[2]/div[1]/div/div'

    while(chat_loading == True):
        exist_element(by=[By.XPATH, By.XPATH], element_info=[CHAT_GET_TEXT_XPATH, CHAT_NETWORK_ERROR],
                       event=[['is_loading(element.get_attribute("class"))'], ['refrash()', 'driver.implicitly_wait(10)', f'give_text({before_text})']])

    exist_element(by=[By.XPATH], element_info=[CHAT_GET_TEXT_XPATH], event=[['extract_text(element)']])

    num+=2

def extract_text(element):
    n = 1
    p = element.find_elements(By.TAG_NAME, 'p')
    for i in p:
        li = i.find_element(By.XPATH, '..').tag_name
        if(li == 'li'):
            print(f'{n}. {i.text}\n')
            n+=1
        else:
            print(f'{i.text}\n')
    return

def chat_logout():
    pass

def refrash():
    driver.refresh()
    return

def login_pass_cloudflare(element):
    element.click()
    exist_element(by=[By.XPATH], element_info=[CHAT_LOGIN_XPATH], event=[['element.click()']]) 
    return

def pass_cloudflare(element):
    element.click()
    return

def main():
    global before_text
    cheak()
    chat_login()
    pass_comment()
    while(1):
        text = input(">> query : ")
        before_text = text
        print('\n')
        give_text(text)
        get_text()

main()