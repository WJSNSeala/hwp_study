# HWP 분석

hwp format 분석을 통해 스크립트 삽입 테스트 목적


## 1. 자료형 설명
한 바이트 8bit -> little-endian 사용   
배열의 경우 자료형 array[개수]로 표현.   

WORD array[10]    

BYTE 1 부호 없는 한 바이트(0～255)   
WORD 2 16비트 컴파일러에서 ‘unsigned int’에 해당   
DWORD 4 16비트 컴파일러에서 ‘unsigned long’에 해당   
WCHAR 2 글의 기본 코드로 유니코드 기반 문자   
HWPUNIT 4 1/7200인치로 표현된 글 내부 단위   
SHWPUNIT 4  1/7200인치로 표현된 글 내부 단위   
UINT8 1 unsigned __int8 에 해당   
UINT16 2 ‘unsigned __int16’ 에 해당   
UINT32(=UINT) 4 ‘unsigned __int32 에 해당   
INT8 1  ‘signed __int8’ 에 해당   
INT16 2  ‘signed __int16’ 에 해당   
INT32 4  ‘signed __int32’ 에 해당   
HWPUNIT16 2  INT16 과 같다. COLORREF 4 RGB값(0x00bbggrr)을 십진수로 표시   
(rr : red 1 byte, gg : green 1 byte, bb : blue 1 byte)   
BYTE stream 일련의 BYTE로 구성됨. 본문 내에서 다른 구조를 참조할 경우에 사용됨.   

WCHAR는 한글의 내부 코드로 표현된 문자 한 글자를 표현하는 자료형이다. 한글의 내부 코드는 한글, 영문, 한자를 비롯해 모든 문자가 2 바이트의 일정한 길이를 가진다.      
[가로 2 인치 x 세로 1 인치]짜리 그림의 크기를 HWPUNIT 형으로 표현하면 각각 14400 x 7200이 된다.   

## 2. 한글 파일 구조

### 2.1 한글 파일 구조 요약

복합 파일 Compund File 구조를 가진다. -> 내부적으로 storage, stream을 구별하기 위한 이름을 가짐    

### 2.2 스토리지별 저장 정보

#### 2.2.1 파일 인식 정보
한글 문서 파일이라는 것을 나타내기 위해 파일 인식 정보를 저장.   
FileHeader stream에 저장되는 데이터는 다음과 같다.

| 자료형            | 길이                  | 설명                           |
|-----------------|-----------------------|-------------------------------|
| BYTE array[32]  | 32 | signature : 문서 파일은 HWP DOcument File  |
| DWORD  | 4 | 파일 버전 : 0xMMnnPPrr의 형태 (5.0.3.0)  MM, nn숫자가 다르면 호환 불가능 |
| DWORD 4 | 속성 |  | 범위 | 설명 | 
                    |bit 0 | 압축 여부| 
bit 1 암호 설정 여부
bit 2 배포용 문서 여부
bit 3 스크립트 저장 여부
bit 4 DRM 보안 문서 여부
bit 5 XMLTemplate 스토리지 존재 여부
bit 6 문서 이력 관리 존재 여부
bit 7 전자 서명 정보 존재 여부
bit 8 공인 인증서 암호화 여부
bit 9 전자 서명 예비 저장 여부
bit 10 공인 인증서 DRM 보안 문서 여부
bit 11 CCL 문서 여부
bit 12 모바일 최적화 여부
bit 13 개인 정보 보안 문서 여부
bit 14 변경 추적 문서 여부
bit 15 공공누리(KOGL) 저작권 문서
bit 16 비디오 컨트롤 포함 여부
bit 17 차례 필드 컨트롤 포함 여부
bit 18～31 예약  |



