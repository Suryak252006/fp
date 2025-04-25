import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==== SETUP ====
community_name = "MentiBY-Cohort 2.0"
subgroup_name = "Basic"
numbers = input("Paste comma-separated mobile numbers (with country code): ").split(',')

processed_file = "processed_numbers.txt"
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        processed_numbers = set(line.strip() for line in f)
else:
    processed_numbers = set()

# ==== LAUNCH BROWSER ====
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
wait = WebDriverWait(driver, 60)

# ==== WAIT FOR LOGIN ====
print("🔐 Waiting for WhatsApp Web login...")
while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        print("✅ Logged into WhatsApp Web.")
        break
    except:
        print("📱 Still waiting for login...")
        time.sleep(5)

# ==== OPEN COMMUNITY AND BASIC GROUP via Manage Community ====
def open_basic_group():
    try:
        # Search for community
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        search_box.send_keys(community_name)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        print(f"✅ Opened community chat: {community_name}")

        # Click "Manage community"
        try:
            manage_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Manage community"]')))
            manage_btn.click()
            print("✅ Clicked 'Manage community'.")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not click 'Manage community': {str(e)}")
            return False

        # Click "View groups"
        try:
            view_groups_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@title="View groups"]')))
            view_groups_btn.click()
            print("✅ Clicked 'View groups'.")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Could not click 'View groups': {str(e)}")
            return False

        # Click "Basic" group in list
        try:
            basic_group = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{subgroup_name}"]')))
            basic_group.click()
            print(f"✅ Entered subgroup: {subgroup_name}")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Could not click subgroup '{subgroup_name}': {str(e)}")
            return False

        return True

    except Exception as e:
        print(f"❌ General failure in open_basic_group: {str(e)}")
        return False

# ==== ADD OR INVITE FUNCTION ====
def add_or_invite(number):
    try:
        header = wait.until(EC.presence_of_element_located((By.XPATH, '//header')))
        header.click()
        time.sleep(2)

        add_btn_xpath = '//div[contains(@aria-label, "Add participant") or contains(@title, "Add participant")]'
        add_participant_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_btn_xpath)))
        add_participant_btn.click()
        time.sleep(2)

        participant_search = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        participant_search.clear()
        participant_search.send_keys(number.strip())
        time.sleep(3)

        try:
            user_xpath = '//span[@title][@dir="auto"]'
            user = wait.until(EC.element_to_be_clickable((By.XPATH, user_xpath)))
            user.click()
            time.sleep(1)

            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="add-participant-confirm-button"]')))
            confirm_btn.click()
            print(f"✅ Added {number.strip()} to the group.")
        except:
            try:
                invite_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Invite to group via link"]')))
                invite_btn.click()
                print(f"⚠️ Sent invite to {number.strip()} (direct add not possible).")
            except:
                print(f"❌ Could not add or invite {number.strip()}.")

        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="x-viewer"]')))
            close_btn.click()
            time.sleep(1)
        except:
            print("⚠️ Could not close group info panel.")

        with open(processed_file, "a") as f:
            f.write(number.strip() + "\n")
        processed_numbers.add(number.strip())

        time.sleep(10)

    except Exception as e:
        print(f"❌ Error with {number.strip()}: {str(e)}")

# ==== MAIN EXECUTION ====
if open_basic_group():
    for num in numbers:
        if num.strip() in processed_numbers:
            print(f"⏩ Skipping {num.strip()} (already processed)")
            continue
        add_or_invite(num)

print("🎉 Done adding/inviting all students!")
driver.quit()
