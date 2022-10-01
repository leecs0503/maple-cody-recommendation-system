# WzComparerR2Server
WzComparerR2 API 서버

# Installation
```
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-6.0
sudo apt install libc6-dev 
sudo apt install libgdiplus
dotnet dev-certs https -ep $/https/aspnetapp.pfx -p {password}
dotnet dev-certs https --trust
```

# 실행
```
dotnet run
docker-compose up
```

# Route 구조

## /code/
wz파일 내부의 모든 파일을 json포맷으로 리턴하는 route

## /avatar_raw/
아바타 코드와 캐릭터의 actionName을 받아서 png형식으로 리턴하는 route

 - 예시 : /avatar_raw/?code=2000,12000,21000,31000,,1041046,,1061039&actionName=stand1&earType=ear

|query parameter|description|
|:---:|---|
|code|WzComparerR2의 아바타 기능에서 사용하는 있는 코드 포맷에 따른 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
|earType|아바타의 귀 종류, ear, humanEar, lefEar, highlefEar 중 하나. default로는 humanEar|

## /avatar/
avatar_raw와 동일한 작업을 하는 route.

 - 예시 : /avatar/?head=12015&face=21078&hair=41750%2B5*50&cap=1004898&longcoat=1051513&shoes=1071103&glove=1082002&shield=1092008&cape=1102988&weapon=1702736&earrings=1032200&faceAccessory=1012757&eyeAccessory=1022277&actionName=stand1&earType=ear

|query parameter|description|example|
|:---:|---|---|
|head|피부에 대한 코드.|head=12015|
|face|얼굴 성형에 대한 코드.|face=21078|
|hair|헤어에 대한 코드. 믹스 염색 또한 가능.|hair=41750%2B5*50|
|cap|모자에 대한 코드.|cap=1004898|
|coat|상의에 대한 코드.|coat=1042254|
|longcoat|전신옷에 대한 코드.|longcoat=1051513|
|pants|하의에 대한 코드.|pants=1062165|
|shoes|신발에 대한 코드.|shoes=1071103|
|glove|장갑에 대한 코드.|glove=1082002|
|shield|방패 또는 보조무기에 대한 코드.|shield=1092008|
|cape|망토에 대한 코드.|cape=1102988|
|waepon|무기에 대한 코드.|weapon=1702736|
|earrings|귀고리에 대한 코드.|earrings=1032200|
|faceAccessory|얼굴 장식에 대한 코드.|faceAccessory=1012757|
|eyeAccessory|눈장식에 대한 코드.|eyeAccessory=1022277|
|actionName|avatar_raw와 동일.|actionName=stand1|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
|earType|아바타의 귀 종류, ear, humanEar, lefEar, highlefEar 중 하나. default로는 humanEar|

## /head/
피부에 대한 개별 이미지를 리턴하는 route.

- 예시 : /head/?code=12015&actionName=stand1&earType=ear

|query parameter|description|
|:---:|---|
|code|피부 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
|earType|아바타의 귀 종류, ear, humanEar, lefEar, highlefEar 중 하나. default로는 humanEar|

## /face/
얼굴 성형에 대한 개별 이미지를 리턴하는 route.

 - 예시 :  /face/?code=21078

|query parameter|description|
|:---:|---|
|code|얼굴 성형 아이템 코드.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /hair/
헤어에 대한 개별 이미지를 리턴하는 route. 모자쓴 상태의 머리 이미지를 리턴함.

 - 예시 : /hair/?code=41750%2B5*50&actionName=stand1

|query parameter|description|
|:---:|---|
|code|헤어 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
## /hearoverhead/
헤어에 대한 개별 이미지를 리턴하는 route. 원래 상태의 머리 이미지를 리턴함.

 - 예시 : /hairoverhead/?code=41750%2B5*50&actionName=stand1

|query parameter|description|
|:---:|---|
|code|헤어 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
## /cap/
모자에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /cap/?code=1004898&actionName=stand1

|query parameter|description|
|:---:|---|
|code|모자 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /coat/
상의에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /coat/?code=1042254&actionName=stand1

|query parameter|description|
|:---:|---|
|code|상의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|
## /longcoat/
전신옷에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /longcoat/?code=1051513&actionName=stand1

|query parameter|description|
|:---:|---|
|code|전신옷의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /pants/
하의에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /pants/?code=1062165&actionName=stand1

|query parameter|description|
|:---:|---|
|code|하의의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /shoes/
신발에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /shoes/?code=1071103&actionName=stand1

|query parameter|description|
|:---:|---|
|code|신발의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /lglove/
왼손 장갑에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /lglove/?code=1082002&actionName=stand1

|query parameter|description|
|:---:|---|
|code|장갑의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /rglove/
오른손 장갑에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /rglove/?code=1082002&actionName=stand1

|query parameter|description|
|:---:|---|
|code|장갑의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /shield/
방패 또는 보조무기에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /shield/?code=1092008&actionName=stand1

|query parameter|description|
|:---:|---|
|code|방패의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /cape/
망토에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /cape/?code=1102988&actionName=stand1

|query parameter|description|
|:---:|---|
|code|망토의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /weapon/
무기에 대한 개별 이미지를 리턴하는 route. 무기 타입에 맞는 actionName을 줄 필요가 있음.

 - 예시 : /weapon/?code=1702736&actionName=stand1

|query parameter|description|
|:---:|---|
|code|무기의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /earrings/
귀고리에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /earrings/?code=1032200&actionName=stand1

|query parameter|description|
|:---:|---|
|code|귀고리의 아이템 코드.|
|actionName|캐릭터의 모션을 지정. stand1(한손무기 모션) 또는 stand2(두손무기 모션)만을 받음. default로는 stand1.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /faceAccessory/
얼굴 장식에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /faceAccessory/?code=1012757

|query parameter|description|
|:---:|---|
|code|얼굴 장식의 아이템 코드.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|

## /eyeAccessory/
눈 장식에 대한 개별 이미지를 리턴하는 route.

 - 예시 : /eyeAccessory/?code=1022277

|query parameter|description|
|:---:|---|
|code|눈 장식의 아이템 코드.|
|bs|이미지를 base64 encoding한 문자열로 리턴할지 결정하는 boolean variable. default로는 false|