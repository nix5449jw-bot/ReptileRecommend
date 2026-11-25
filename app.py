import streamlit as st
import random
import requests

# 페이지 기본 설정
st.set_page_config(page_title="나만의 반려 양서·파충류 추천기", page_icon="🦎", layout="centered")

# ==============================================================================
# [필수 구문 1: 리스트(list)] 총 51종의 파충류/양서류/거북류 데이터베이스 (학명 포함)
# ==============================================================================
PETS_DB = [
    # --- 붙이류/야행성 게코 ---
    {"name": "크레스티드 게코", "sci_name": "Correlophus ciliatus", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 10, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "활동적이고 교감을 원함", "느긋하고 귀차니즘이 있음"], "desc": "속눈썹이 매력적이며 전용 가루 사료(슈퍼푸드)로 사육이 가능해 입문자에게 인기가 많습니다.", "tip": "적정 습도(60~80%) 유지를 위해 하루 1~2회 분무해 주세요."},
    {"name": "모어닝 게코", "sci_name": "Lepidodactylus lugubris", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 2, "min_home": 3, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "암컷 혼자서도 번식(단위생식)하는 작고 귀여운 관상용 게코입니다.", "tip": "크기가 매우 작아 사육장 틈새로 탈출하지 않도록 주의해야 합니다."},
    {"name": "가고일 게코", "sci_name": "Rhacodactylus auriculatus", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "악어 같은 외모와 뿔이 특징인 붙이류 도마뱀으로 크레스티드 게코와 사육법이 비슷합니다.", "tip": "발톱 힘이 강하므로 나무 껍질이나 유목을 많이 넣어주세요."},
    {"name": "리키에너스", "sci_name": "Rhacodactylus leachianus", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "세계에서 가장 큰 게코 중 하나로, 묵직한 크기와 쭈글쭈글한 피부가 매력적입니다.", "tip": "성체가 되면 영역 본능이 강해질 수 있어 단독 사육을 권장합니다."},
    {"name": "차화 게코", "sci_name": "Mniarogekko chahoua", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "활동적이고 교감을 원함"], "desc": "이끼 같은 보호색과 꼬리를 감는 습성이 특징인 매력적인 붙이류 게코입니다.", "tip": "칼슘 요구량이 높으므로 슈퍼푸드와 함께 칼슘제를 묻힌 곤충을 급여하세요."},
    {"name": "카멜레온 게코", "sci_name": "Eurydactylodes agricolae", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "작은 카멜레온을 닮은 독특한 외모의 소형 게코입니다.", "tip": "높은 습도와 통풍의 균형을 잘 맞추는 것이 중요합니다."},
    {"name": "레오파드 게코", "sci_name": "Eublepharis macularius", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 10, "max_away": 3, "min_home": 3, "personalities": ["차분하고 꼼꼼함", "활동적이고 교감을 원함", "느긋하고 귀차니즘이 있음"], "desc": "웃는 듯한 입매와 순한 성격으로 전 세계에서 가장 사랑받는 입문용 도마뱀입니다.", "tip": "바닥재 온도를 30도 내외로 따뜻하게 유지해 소화를 도와주세요."},
    {"name": "팻테일 게코", "sci_name": "Hemitheconyx caudicinctus", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 10, "max_away": 3, "min_home": 3, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "통통한 꼬리와 초콜릿색 줄무늬가 귀여운 온순한 지상성 게코입니다.", "tip": "레오파드 게코보다 습도를 약간 더 높게(50~60%) 유지해 주세요."},
    {"name": "피쉬스케일 게코", "sci_name": "Geckolepis maculata", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음"], "desc": "위협을 받으면 물고기 비늘처럼 피부를 벗어던지고 도망가는 신기한 습성을 가졌습니다.", "tip": "피부가 매우 약하므로 절대 손으로 잡는 핸들링을 하지 마세요."},
    {"name": "납테일 게코", "sci_name": "Nephrurus levis", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 3, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "큰 머리와 동그란 눈, 꼬리 끝의 작은 뭉치가 매력적인 사막성 게코입니다.", "tip": "땅을 파는 습성이 있으므로 모래 바닥재를 두껍게 깔아주세요."},
    {"name": "토케이 게코", "sci_name": "Gekko gecko", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 15, "max_away": 2, "min_home": 4, "personalities": ["호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음"], "desc": "화려한 푸른빛 몸에 주황색 반점이 있는 대형 게코로, '토케이'하고 우는 소리가 특징입니다.", "tip": "성격이 사납고 물 힘이 강하므로 관상 위주로 사육하는 것이 좋습니다."},

    # --- 스킨크/드래곤/모니터/카멜레온 ---
    {"name": "레드아이 아머드 스킨크", "sci_name": "Tribolonotus gracilis", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 13, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "눈 주위의 붉은 테두리와 용의 비늘 같은 등갑이 멋진 소형 스킨크입니다.", "tip": "겁이 매우 많으므로 은신처를 충분히 만들어주고 고습도 환경을 유지하세요."},
    {"name": "화이트아이 아머드 스킨크", "sci_name": "Tribolonotus novaeguineae", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 13, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "눈 주위가 하얀색을 띠는 아머드 스킨크로, 미니 드래곤 같은 외모가 매력입니다.", "tip": "조용하고 어두운 환경을 좋아하며 높은 습도가 필수입니다."},
    {"name": "파이어 스킨크", "sci_name": "Lepidothyris fernandi", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "옆구리의 불타는 듯한 붉은색과 검은색 무늬가 화려한 지상성 스킨크입니다.", "tip": "바닥재 속으로 파고드는 것을 좋아하므로 에코어스 등을 깊게 깔아주세요."},
    {"name": "블루텅 스킨크", "sci_name": "Tiliqua scincoides", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 13, "max_away": 2, "min_home": 5, "personalities": ["활동적이고 교감을 원함", "차분하고 꼼꼼함"], "desc": "파란색 혀를 내미는 순하고 튼튼한 중형 도마뱀으로, 잡식성이라 먹이 급여가 수월합니다.", "tip": "몸길이가 길어지므로 최소 3자(90cm) 이상의 넓은 사육장이 필요합니다."},
    {"name": "술라웨시 워터 스킨크", "sci_name": "Tropidophorus baconi", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 5, "personalities": ["호기심이 많고 도전을 즐김", "차분하고 꼼꼼함"], "desc": "수영을 즐기는 반수생 스킨크로, 활동적인 모습을 관찰하는 재미가 있습니다.", "tip": "사육장 내에 몸을 담글 수 있는 넓은 물그릇과 여과 환경을 마련해 주세요."},
    {"name": "선 스킨크", "sci_name": "Eutropis multifasciata", "type": "파충류(도마뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 2, "min_home": 4, "personalities": ["느긋하고 귀차니즘이 있음", "호기심이 많고 도전을 즐김"], "desc": "햇빛을 받으면 무지개빛 광택이 나는 매끈한 비늘을 가진 날렵한 도마뱀입니다.", "tip": "움직임이 매우 빠르므로 사육장 문을 열 때 탈출하지 않도록 주의하세요."},
    {"name": "비어디 드래곤", "sci_name": "Pogona vitticeps", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 13, "max_away": 2, "min_home": 6, "personalities": ["활동적이고 교감을 원함", "차분하고 꼼꼼함"], "desc": "주인을 잘 알아보고 핸들링이 매우 순해 '파충류계의 강아지'로 불립니다.", "tip": "강한 UVB 조명과 스팟 램프, 매일 신선한 채소와 곤충 급여가 필요합니다."},
    {"name": "목도리 도마뱀", "sci_name": "Chlamydosaurus kingii", "type": "파충류(도마뱀)", "difficulty": "숙련자", "min_age": 15, "max_away": 1, "min_home": 6, "personalities": ["호기심이 많고 도전을 즐김", "활동적이고 교감을 원함"], "desc": "목 주변의 커다란 프릴을 펼치는 모습과 두 발로 달리는 행동이 인상적인 도마뱀입니다.", "tip": "나무 위에서 생활하므로 높이가 높은 대형 사육장과 UVB 조명이 필수입니다."},
    {"name": "레그리스 리자드", "sci_name": "Pseudopus apodus", "type": "파충류(도마뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 3, "min_home": 4, "personalities": ["호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음"], "desc": "뱀처럼 다리가 없지만 눈꺼풀과 귓구멍이 있는 신기한 무족 도마뱀입니다.", "tip": "뱀과 달리 턱이 벌어지지 않으므로 귀뚜라미나 달팽이 등 작은 먹이를 주세요."},

    # --- 모니터(왕도마뱀) ---
    {"name": "액키 모니터", "sci_name": "Varanus acanthurus", "type": "파충류(왕도마뱀)", "difficulty": "입문자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["활동적이고 교감을 원함", "호기심이 많고 도전을 즐김", "차분하고 꼼꼼함"], "desc": "성체 크기가 60~70cm 정도로 작아 가정에서 키우기 가장 적합한 소형 왕도마뱀입니다.", "tip": "핫존 온도를 50도 이상으로 높게 설정해주면 매우 활발하게 움직입니다."},
    {"name": "사바나 모니터", "sci_name": "Varanus exanthematicus", "type": "파충류(왕도마뱀)", "difficulty": "중급자", "min_age": 15, "max_away": 2, "min_home": 5, "personalities": ["활동적이고 교감을 원함", "호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음"], "desc": "묵직한 체형과 온순한 성격을 가진 아프리카 출신 왕도마뱀으로 핸들링 교감이 가능합니다.", "tip": "비만이 되기 쉬우므로 설치류 대신 곤충 위주의 식단과 산책을 챙겨주세요."},
    {"name": "알거스 모니터", "sci_name": "Varanus panoptes", "type": "파충류(왕도마뱀)", "difficulty": "중급자", "min_age": 15, "max_away": 2, "min_home": 5, "personalities": ["호기심이 많고 도전을 즐김", "활동적이고 교감을 원함"], "desc": "뒷다리로 서서 주변을 살피는 '삼각대 자세'가 유명한 지능 높은 왕도마뱀입니다.", "tip": "활동량이 많고 크게 자라므로 넉넉한 사육 공간과 깊이 파고들 바닥재를 주세요."},
    {"name": "워터 모니터", "sci_name": "Varanus salvator", "type": "파충류(왕도마뱀)", "difficulty": "숙련자", "min_age": 16, "max_away": 1, "min_home": 6, "personalities": ["호기심이 많고 도전을 즐김", "활동적이고 교감을 원함", "차분하고 꼼꼼함"], "desc": "지능이 매우 높고 수영을 잘하며 주인과 교감도 가능하지만 초대형으로 자라는 왕도마뱀입니다.", "tip": "성체가 2m 내외로 크므로 대형 물공간과 넓은 실내 사육 환경을 준비해야 합니다."},
    {"name": "나일 모니터", "sci_name": "Varanus niloticus", "type": "파충류(왕도마뱀)", "difficulty": "숙련자", "min_age": 16, "max_away": 1, "min_home": 6, "personalities": ["호기심이 많고 도전을 즐김", "차분하고 꼼꼼함"], "desc": "화려한 황금빛 점무늬를 가졌지만 야생성이 강하고 카리스마 넘치는 대형 왕도마뱀입니다.", "tip": "꼬리 치기와 물림에 주의해야 하며, 어릴 때부터 꾸준히 신뢰를 쌓는 것이 중요합니다."},

    {"name": "베일드 카멜레온", "sci_name": "Chamaeleo calyptratus", "type": "파충류(도마뱀)", "difficulty": "숙련자", "min_age": 15, "max_away": 1, "min_home": 7, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "머리 위의 높은 볏(카스크)과 기분에 따라 변하는 체색이 신비로운 카멜레온입니다.", "tip": "고인 물을 먹지 않으므로 드리퍼로 물방울을 떨어뜨려 주고 통풍에 신경 쓰세요."},
    {"name": "팬서 카멜레온", "sci_name": "Furcifer pardalis", "type": "파충류(도마뱀)", "difficulty": "숙련자", "min_age": 15, "max_away": 1, "min_home": 7, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "출신 지역(로칼)에 따라 무지개처럼 화려한 발색을 보여주는 카멜레온의 제왕입니다.", "tip": "스트레스에 민감하므로 메쉬 케이지에 살아있는 식물을 배치해 은신처를 만들어주세요."},

    # --- 뱀류 ---
    {"name": "콘 스네이크", "sci_name": "Pantherophis guttatus", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 5, "min_home": 2, "personalities": ["느긋하고 귀차니즘이 있음", "활동적이고 교감을 원함"], "desc": "온순한 성격과 다양한 색상, 주 1회 급여의 편리함으로 최고의 입문용 뱀으로 꼽힙니다.", "tip": "좁은 틈으로 빠져나가는 탈출의 명수이므로 사육장 잠금장치를 꼭 확인하세요."},
    {"name": "호그노즈 스네이크", "sci_name": "Heterodon nasicus", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 14, "max_away": 4, "min_home": 3, "personalities": ["활동적이고 교감을 원함", "호기심이 많고 도전을 즐김"], "desc": "돼지코처럼 들린 주둥이가 귀엽고, 위협을 느끼면 죽은 척 연기하는 개성 만점 뱀입니다.", "tip": "약한 독(후아독)이 있지만 사람에게는 무해하며, 겁이 많아 거식할 때가 있습니다."},
    {"name": "볼 파이톤", "sci_name": "Python regius", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 4, "min_home": 3, "personalities": ["느긋하고 귀차니즘이 있음", "차분하고 꼼꼼함", "활동적이고 교감을 원함"], "desc": "위험을 느끼면 공처럼 몸을 마는 온순한 비단뱀으로, 수백 가지의 아름다운 모프와 튼튼한 생명력을 자랑합니다.", "tip": "환경 변화에 예민해 간혹 거식을 할 수 있으므로 온도와 습도를 일정하게 유지하세요."},
    {"name": "킹 스네이크", "sci_name": "Lampropeltis getula", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 13, "max_away": 5, "min_home": 2, "personalities": ["느긋하고 귀차니즘이 있음", "호기심이 많고 도전을 즐김"], "desc": "먹성이 매우 뛰어나 거식 걱정이 거의 없고 튼튼한 입문용 뱀입니다.", "tip": "다른 뱀을 잡아먹는 습성이 있으므로 반드시 한 마리씩 단독 사육해야 합니다."},
    {"name": "밀크 스네이크", "sci_name": "Lampropeltis triangulum", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 13, "max_away": 5, "min_home": 2, "personalities": ["느긋하고 귀차니즘이 있음", "호기심이 많고 도전을 즐김"], "desc": "독사인 산호뱀을 흉내 낸 붉은색·검은색·흰색의 화려한 띠무늬가 매력적인 온순한 뱀입니다.", "tip": "어릴 때는 예민해서 꼬리를 떨거나 배설물을 뿌릴 수 있지만 크면서 순해집니다."},
    {"name": "랫 스네이크", "sci_name": "Pantherophis obsoletus", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 14, "max_away": 5, "min_home": 3, "personalities": ["느긋하고 귀차니즘이 있음", "호기심이 많고 도전을 즐김"], "desc": "활동성이 좋고 튼튼하며, 성장 속도가 빠르고 시원시원한 크기로 자라는 뱀입니다.", "tip": "나무를 잘 타므로 유목을 넣어주면 입체적으로 움직이는 모습을 볼 수 있습니다."},
    {"name": "불 스네이크", "sci_name": "Pituophis catenifer sayi", "type": "파충류(뱀)", "difficulty": "중급자", "min_age": 15, "max_away": 4, "min_home": 3, "personalities": ["호기심이 많고 도전을 즐김"], "desc": "성체가 2m 가까이 자라는 대형 콜루브리드 뱀으로, 위협 시 쉭쉭거리는 큰 소리를 냅니다.", "tip": "소리는 무섭지만 실제로는 온순한 편이며, 큰 체격에 맞는 넓은 사육장이 필요합니다."},
    {"name": "하우스 스네이크", "sci_name": "Boaedon fuliginosus", "type": "파충류(뱀)", "difficulty": "입문자", "min_age": 12, "max_away": 5, "min_home": 2, "personalities": ["느긋하고 귀차니즘이 있음", "차분하고 꼼꼼함"], "desc": "아프리카 출신의 소형 뱀으로, 크기가 작고 온순하며 무지개빛 광택이 아름답습니다.", "tip": "작은 설치류를 잘 먹으며 사육 난이도가 매우 낮아 초보자에게 좋습니다."},
    {"name": "가터 스네이크", "sci_name": "Thamnophis sirtalis", "type": "파충류(뱀)", "difficulty": "중급자", "min_age": 14, "max_away": 3, "min_home": 4, "personalities": ["호기심이 많고 도전을 즐김", "차분하고 꼼꼼함"], "desc": "설치류 대신 미꾸라지, 지렁이, 개구리 등을 먹는 식성을 가진 날렵한 뱀입니다.", "tip": "신진대사가 빨라 다른 뱀보다 먹이를 자주(주 2회 정도) 주어야 합니다."},

    # --- 양서류 ---
    {"name": "팩맨 개구리", "sci_name": "Ceratophrys cranwelli", "type": "양서류(개구리)", "difficulty": "입문자", "min_age": 10, "max_away": 3, "min_home": 3, "personalities": ["느긋하고 귀차니즘이 있음"], "desc": "게임 캐릭터 '팩맨'처럼 커다란 입과 동그란 몸매를 가진 인기 양서류입니다.", "tip": "움직임이 거의 없어 좁은 곳에서도 키울 수 있지만, 피부 보호를 위해 핸들링은 피하세요."},
    {"name": "버젯 프로그", "sci_name": "Lepidobatrachus laevis", "type": "양서류(개구리)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 4, "personalities": ["호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음"], "desc": "납작하고 넙적한 얼굴과 괴성을 지르는 독특한 방어 행동으로 유명한 수생 개구리입니다.", "tip": "수질 관리가 중요하며, 턱 힘이 매우 강하므로 급여 시 핀셋을 꼭 사용하세요."},
    {"name": "픽시 프로그", "sci_name": "Pyxicephalus adspersus", "type": "양서류(개구리)", "difficulty": "입문자", "min_age": 12, "max_away": 3, "min_home": 3, "personalities": ["호기심이 많고 도전을 즐김", "느긋하고 귀차니즘이 있음", "차분하고 꼼꼼함"], "desc": "성체 수컷이 20cm 이상 거대하게 자라는 '아프리카 황소개구리'로, 튼튼하고 먹성이 좋아 키우는 재미가 큽니다.", "tip": "엄청난 대식가이므로 비만이 되지 않도록 먹이 양을 조절해 주세요."},
    {"name": "팩꽁이 (판타지 프로그)", "sci_name": "Ceratophrys ornata", "type": "양서류(개구리)", "difficulty": "입문자", "min_age": 10, "max_away": 3, "min_home": 3, "personalities": ["느긋하고 귀차니즘이 있음", "차분하고 꼼꼼함"], "desc": "팩맨 개구리와 버젯 프로그의 교잡종으로, 두 종의 귀여운 특징을 모두 가졌습니다.", "tip": "사육법은 팩맨 개구리와 동일하며, 촉촉한 바닥재와 깨끗한 물그릇을 유지해 주세요."},
    {"name": "사막비 개구리", "sci_name": "Breviceps macrops", "type": "양서류(개구리)", "difficulty": "숙련자", "min_age": 15, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "화났을 때 삑삑거리는 장난감 같은 울음소리와 둥근 몸매로 SNS에서 큰 인기를 끈 개구리입니다.", "tip": "야생 채집 개체가 많고 환경 세팅(특수 모래, 습도 조절)이 매우 까다로운 편입니다."},
    {"name": "청개구리", "sci_name": "Dryophytes japonicus", "type": "양서류(개구리)", "difficulty": "입문자", "min_age": 10, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "우리 주변에서도 볼 수 있는 친숙하고 귀여운 초록빛 나무개구리입니다.", "tip": "밤에 수컷이 큰 소리로 울 수 있으며, 수돗물은 염소를 제거한 뒤 사용해 주세요."},
    {"name": "화이트 트리 프록", "sci_name": "Litoria caerulea", "type": "양서류(개구리)", "difficulty": "입문자", "min_age": 12, "max_away": 2, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "웃는 입매와 통통한 손가락, 튼튼한 생명력으로 가장 추천되는 입문용 청개구리입니다.", "tip": "먹성이 좋아 살이 찌기 쉬우므로 적정 급여량을 지켜주세요."},
    {"name": "밀키 프록", "sci_name": "Trachycephalus resinifictrix", "type": "양서류(개구리)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "우윳빛 피부와 파란색 입안, 발가락이 마치 장난감 피규어처럼 예쁜 아마존 개구리입니다.", "tip": "높은 습도와 청결한 수질이 중요하며, 스트레스를 받으면 하얀 점액을 분비합니다."},
    {"name": "아홀로틀 (우파루파)", "sci_name": "Ambystoma mexicanum", "type": "양서류(도롱뇽)", "difficulty": "중급자", "min_age": 12, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "핑크빛 몸과 겉아가미가 사랑스러운 수생 도롱뇽입니다.", "tip": "고온에 매우 취약하므로 여름철에는 냉각팬이나 냉각기를 이용해 수온을 20도 이하로 낮춰주세요."},
    {"name": "파이어밸리 뉴트", "sci_name": "Cynops pyrrhogaster", "type": "양서류(도롱뇽)", "difficulty": "입문자", "min_age": 12, "max_away": 3, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "검은 등에 불타는 듯한 붉은 배를 가진 작고 튼튼한 수생 도롱뇽입니다.", "tip": "물 밖으로 나올 수 있는 육지 공간을 함께 만들어주고 수온을 시원하게 유지하세요."},
    {"name": "파이어 살라만다", "sci_name": "Salamandra salamandra", "type": "양서류(도롱뇽)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "호기심이 많고 도전을 즐김"], "desc": "검은 몸에 선명한 노란색 반점이 인상적인 육상 도롱뇽으로 수명이 매우 깁니다.", "tip": "더위에 약하므로 서늘하고 습한 환경을 만들어주어야 합니다."},

    # --- 거북류 ---
    {"name": "커먼 머스크 터틀", "sci_name": "Sternotherus odoratus", "type": "파충류(반수생거북)", "difficulty": "입문자", "min_age": 12, "max_away": 3, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "성체가 되어도 10~13cm 정도로 작아 어항에서 키우기 좋은 소형 반수생 거북입니다.", "tip": "수영 실력이 서툰 편이므로 물 깊이를 너무 깊지 않게 하고 발이 닿는 육지를 만들어주세요."},
    {"name": "레이져백 터틀", "sci_name": "Sternotherus carinatus", "type": "파충류(반수생거북)", "difficulty": "입문자", "min_age": 12, "max_away": 3, "min_home": 4, "personalities": ["차분하고 꼼꼼함", "느긋하고 귀차니즘이 있음"], "desc": "등갑 중앙이 면도날처럼 뾰족하게 솟아오른 모습이 멋진 소형 반수생 거북입니다.", "tip": "겁이 많은 편이라 유목이나 수초로 숨을 곳을 만들어주면 안정감을 느낍니다."},
    {"name": "페닌술라 워터 쿠터", "sci_name": "Pseudemys peninsularis", "type": "파충류(반수생거북)", "difficulty": "중급자", "min_age": 14, "max_away": 3, "min_home": 5, "personalities": ["활동적이고 교감을 원함", "차분하고 꼼꼼함"], "desc": "노란 줄무늬와 활발한 유영이 매력적인 반수생 거북으로, 주인을 잘 알아봅니다.", "tip": "성체가 30cm 이상 크게 자라므로 대형 어항과 강력한 여과기, UVB 조명이 필수입니다."},
    {"name": "동헤르만 육지거북", "sci_name": "Testudo hermanni", "type": "파충류(육지거북)", "difficulty": "중급자", "min_age": 14, "max_away": 2, "min_home": 5, "personalities": ["차분하고 꼼꼼함", "활동적이고 교감을 원함"], "desc": "수명이 길고 온순하며 엉금엉금 걸어 다니는 모습이 귀여운 대표적인 입문용 육지거북입니다.", "tip": "초식성이므로 매일 신선한 엽채류와 칼슘제를 급여하고 UVB 램프를 켜주어야 합니다."}
]


# ==============================================================================
# [필수 구문 2: 함수(def)] 이미지 불러오기, 별점 계산, 추천 알고리즘 함수
# ==============================================================================
@st.cache_data(show_spinner=False)
def get_pet_image(sci_name):
    """위키백과 공식 API를 이용해 깨지지 않는 실제 생물 사진을 가져오는 함수"""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{sci_name.replace(' ', '_')}"
        headers = {"User-Agent": "ReptileRecommenderStudentProject/1.0"}
        res = requests.get(url, headers=headers, timeout=4)
        if res.status_code == 200:
            data = res.json()
            if "thumbnail" in data and "source" in data["thumbnail"]:
                return data["thumbnail"]["source"]
    except Exception:
        pass
    return None


def get_difficulty_stars(pet):
    """난이도와 케어 요구도를 계산해 최대 5개의 별(⭐)로 반환"""
    if pet["difficulty"] == "입문자":
        score = 1
        if pet["max_away"] <= 2 or pet["min_home"] >= 6:
            score = 2
    elif pet["difficulty"] == "중급자":
        score = 3
        if pet["max_away"] <= 1 or pet["min_home"] >= 6:
            score = 4
    else:
        score = 5

    return "⭐" * score + f" ({score}/5)"


def recommend_pets(age, away_days, home_hours, personality, experience):
    """사용자 조건에 맞는 생물 리스트 반환"""
    if experience == "입문자":
        user_exp_level = 1
    elif experience == "중급자":
        user_exp_level = 2
    else:
        user_exp_level = 3

    matched_list = []

    for pet in PETS_DB:
        if pet["difficulty"] == "입문자":
            pet_exp_level = 1
        elif pet["difficulty"] == "중급자":
            pet_exp_level = 2
        else:
            pet_exp_level = 3

        if (age >= pet["min_age"] and 
            away_days <= pet["max_away"] and 
            home_hours >= pet["min_home"] and 
            personality in pet["personalities"] and 
            user_exp_level >= pet_exp_level):
            matched_list.append(pet)

    return matched_list


# ==============================================================================
# [Streamlit UI 구성] 화면 디자인 및 결과 출력
# ==============================================================================
st.title("🦎 나에게 딱 맞는 양서·파충류 추천기")
st.write("라이프스타일과 성향을 선택하면, 51종의 파충류·양서류·거북 중 가장 잘 어울리는 **최대 5종**을 사진과 함께 추천해 드립니다!")
st.divider()

st.subheader("📋 나의 사육 환경 및 성향 선택")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("1. 나이 (만 나이)", min_value=5, max_value=100, value=17, step=1)
    away_days = st.slider("2. 일주일 중 집을 비우는 횟수 (일)", min_value=0, max_value=7, value=1)
    home_hours = st.slider("3. 하루 평균 집에 있는 시간 (시간)", min_value=1, max_value=24, value=6)

with col2:
    personality = st.selectbox(
        "4. 자신의 성격",
        [
            "차분하고 꼼꼼함",
            "활동적이고 교감을 원함",
            "느긋하고 귀차니즘이 있음",
            "호기심이 많고 도전을 즐김"
        ]
    )
    experience = st.radio(
        "5. 양서·파충류 사육 경력",
        ["입문자", "중급자", "숙련자"]
    )

st.divider()

if st.button("🔍 나에게 맞는 반려생물 5종 추천받기!", use_container_width=True, type="primary"):
    candidates = recommend_pets(age, away_days, home_hours, personality, experience)

    if len(candidates) > 0:
        pick_count = min(5, len(candidates))
        picked_pets = random.sample(candidates, pick_count)
        
        st.balloons()
        st.success(f"🎉 조건에 맞는 총 {len(candidates)}종 중 **{pick_count}종**을 추천해 드립니다!")
        
        for idx, pet in enumerate(picked_pets, start=1):
            stars = get_difficulty_stars(pet)
            
            with st.container(border=True):
                info_col, img_col = st.columns([2, 1])
                
                with info_col:
                    st.markdown(f"### {idx}. 🐾 {pet['name']}")
                    st.markdown(f"**분류:** {pet['type']} &nbsp;|&nbsp; **학명:** *{pet['sci_name']}*  \n**사육 난이도:** {stars}")
                    st.write(pet["desc"])
                    st.info(f"💡 **사육 핵심 팁:** {pet['tip']}")
                
                with img_col:
                    img_url = get_pet_image(pet["sci_name"])
                    if img_url:
                        st.image(img_url, caption=pet["name"], use_container_width=True)
                    else:
                        # 네트워크 차단 시 깨진 이미지 대신 깔끔한 안내 카드 표시
                        st.markdown(
                            f"""
                            <div style="background-color:#f0f2f6; border-radius:10px; padding:30px 10px; text-align:center; color:#555;">
                                <div style="font-size:40px;">🦎</div>
                                <div style="font-size:13px; font-weight:bold; margin-top:8px;">{pet['name']}</div>
                                <div style="font-size:11px; color:#888;">({pet['sci_name']})</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
        if len(candidates) > 5:
            st.caption(f"*(전체 {len(candidates)}종의 후보 중 무작위로 5종이 선정되었습니다. 버튼을 다시 누르면 다른 조합이 추천됩니다!)*")
    else:
        st.warning("😅 입력하신 까다로운 조건에 모두 부합하는 생물을 찾지 못했습니다.")
        st.write("집을 비우는 날을 줄이거나 재택 시간을 늘려서 다시 검색해 보세요!")
