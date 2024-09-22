import matplotlib.pyplot as plt
from typing import Any
import cv2

#
# post_type = int(input("Enter final image type (1 or 2) : "))
# form_type = int(input("Enter form type (1, 2, 3) : "))
#
# game_data = []
#
# for i in range(form_type):
#     game_date = str(input("Enter game date (DD-MM) : "))
#     game_league = str(input("Enter game leagues (league 1 - league 2) : "))
#     teams = str(input("Enter teams names : "))
#     events_and_odds = str(input("Enter events and odds (e.g., 1-2:3.4) : "))
#
#     game_data.append((game_date, game_league, teams, events_and_odds))
#
# type IS_BLURRED = bool
#
# if post_type == 2:
#     IS_BLURRED = True
#
# elif post_type == 1:
#     IS_BLURRED = False
#
# final_info = {
#     "is_blurred" : IS_BLURRED,
#     "form_type" : form_type,
#     "game_info" : game_data
# }

def format_to_str(final_info: dict[str, Any]) -> str:
    final_text_output: str = f""

    for i in range(len(final_info["game_info"])):
        date: str = str(final_info["game_info"][i][0])
        leagues: str = str(final_info["game_info"][i][1])
        teams: str = str(final_info["game_info"][i][2])
        events_Odds: str = str(final_info["game_info"][i][3])
        
        if final_info["is_blurred"] == False:
            final_text_output += f"{date} \n{leagues} \n{teams} \nCorrect Score : {events_Odds} \n\n"

        elif final_info["is_blurred"] == True:
            final_text_output += f"{date} \n{leagues} \n{teams} \nCorrect Score :  \n\n"
    
    return final_text_output

def censor(img: cv2.typing.MatLike, x: int, y: int) -> None:
    font: int = cv2.FONT_HERSHEY_DUPLEX

    censorer_img: cv2.typing.MatLike = cv2.imread("assets/BOT.png", cv2.IMREAD_UNCHANGED)
    
    text_size, _ = cv2.getTextSize("Correct Score", font, 0.9, 2)
    censor_img_x: int = x + text_size[0] + 40
    censor_img_y: int = y - 60
        
    censorer_img = cv2.resize(censorer_img, (100,100))
    height, width = censorer_img.shape[:2]
    
    overlay_color = censorer_img[:, :, :3]
    overlay_alpha = censorer_img[:, :, 3] / 255.0  # Normalize alpha mask
            
    roi = img[censor_img_y:censor_img_y+height, censor_img_x:censor_img_x+width]

    for c in range(0, 3):
        roi[:, :, c] = (1.0 - overlay_alpha) * roi[:, :, c] + overlay_alpha * overlay_color[:, :, c]
        
    img[censor_img_y:censor_img_y + height, censor_img_x:censor_img_x + width] = roi

## TODO : clean up this mess of a code for the love of god jeezes dude ##
def put_text(file_name, final_info) -> None:
    global image_of_choose
    global x
    global y

    image_of_choose = "assets/final_SINGLE.png"

    if final_info["form_type"] != 1:
        image_of_choose = "assets/final_MULTIPLE.png"
   
    final_text_output: str = format_to_str(final_info)

    img: cv2.typing.MatLike = cv2.imread(image_of_choose,1)

    if final_info["form_type"] == 3:
        x,y = (1250, 90)
    elif final_info["form_type"] == 2:
        x,y = (1250, 170)
    elif final_info["form_type"] == 1:
        x,y = (1250, 290)
    
    for _, line in enumerate(final_text_output.split('\n')):
        font: int = cv2.FONT_HERSHEY_DUPLEX

        if final_info["form_type"] == 3:
            y += 60
        else:
            y += 75
        
        cv2.putText(img,f"{line}",(x,y), font, 0.9,(0,0,0),2,cv2.LINE_4)
        
        if final_info["is_blurred"] == True and "Correct Score" in line:
            censor(img, x, y)

    cv2.imwrite(f"{file_name}.jpg", img)

