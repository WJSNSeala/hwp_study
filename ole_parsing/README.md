# OLE : Object Linking and Embedding

## OLE file structure

크게 2개의 블록으로 나누어 진다.  
* header block : 512 bytes
        - 파일 전체의 주요 정보들을 가지고 있다.
* data block : 512 bytes 이상.   
        - Property : storage and stream information 보관  
        - stream data <- 대부분 차지  
        - Big Block Allocation Table (BBAT)  
        - Small Block Allocation Table(SBAT)  
        
## OLE Block의 구조 
OLE 파일을 512bytes씩 나누어 블록 번호를 부여   
제일 첫번째 블록은 -1블록임을 기억해야 한다.

### 주요 항목

#### signature
D0 CF 11 E0 A1 B1 1A E1의 값을 가짐 OLE 파일의 header   
첫 8byte ( 0x0000 ~ 0x0007)  

#### Number of Big Block Allocation Table Depot
44 ~ 47 : 0x002C ~ 0x002F까지의 값
4byte(근데 가변길이임)  
Big Block Allocation Table(BBAT)를 저장하고 있는 저장소(Depot)의  
개수를 나타낸다, 만약 이 숫자가 109보다 크다면 Start block of Extra big block allocation table depot과   
Number of Extra Big Block Allocation Table Depot을 참조해야함  

#### Start block of property
48 ~ 51 : 0x0030 ~ 0x0033  
OLE 파일 내부는 작은 파일 시스템과 같다.  
폴더(storage)와 파일(stream)의 구조를 가짐.  
이들의 정보를 담고 있는 곳이 바로 property 영역임  
이 정보를 가진 블록의 시작 값을 담고 있다.  

#### Start block of Small Block Allocation Table
60~63 : 0x3C ~ 0x3F   
SBAT의 시작 위치.   

#### Number of Small Block Allocation Table Depot
64~ 67 : 0x40 ~  0x43  
SBAT를 보관하고 있는 저장소의 개수   

#### Array of Big Block Allocation Table Depot members
76 : 0x4c ~
Big Block Allocation Table을 가진 Depot의 실제 값들을 저장한 배열   


### Big Block Allocation
Big Block Allocation Table(BBAT)는 OLE내부의 스트림의 위치정보를 저장하고 있으며 모두 링크 구조로 연결.   
BBAT Depot은 BBAT가 저장된 저장소를 의미한다.   

Header에 존재하는 Number of Big Block Allocation Table Depot -> 이 숫자 많큼 Array of Big Block Allocation Table Depots members에 값이 보관  
0x3, 0x53, 0x54, 0x158, 0x159, 0x15a, 0x15b, 0x329, 0x32a에 BBAT 정보가 있음  
각 블록에 차례대로 접근하여 512 bytes씩 읽어 조합한 것이 BBAT이다.
```
1's block
-------------------------------------------------------------------------------
 00000000 : FF FF FF FF FF FF FF FF 04 00 00 00 FD FF FF FF   ................
 00000010 : 05 00 00 00 06 00 00 00 18 00 00 00 2F 00 00 00   ............/...
 00000020 : 09 00 00 00 0A 00 00 00 0B 00 00 00 23 00 00 00   ............#...
 00000030 : 0D 00 00 00 0E 00 00 00 0F 00 00 00 10 00 00 00   ................
 00000040 : 11 00 00 00 12 00 00 00 13 00 00 00 14 00 00 00   ................
 00000050 : 15 00 00 00 16 00 00 00 17 00 00 00 FE FF FF FF   ................
 00000060 : 19 00 00 00 1A 00 00 00 1B 00 00 00 1C 00 00 00   ................
 00000070 : 1D 00 00 00 1E 00 00 00 1F 00 00 00 20 00 00 00   ............ ...
 00000080 : 21 00 00 00 22 00 00 00 FE FF FF FF 24 00 00 00   !...".......$...
 00000090 : 25 00 00 00 26 00 00 00 27 00 00 00 28 00 00 00   %...&...'...(...
 000000A0 : 29 00 00 00 2A 00 00 00 2B 00 00 00 2C 00 00 00   )...*...+...,...
 000000B0 : 2D 00 00 00 2E 00 00 00 30 00 00 00 3E 00 00 00   -.......0...>...
 000000C0 : 31 00 00 00 32 00 00 00 33 00 00 00 34 00 00 00   1...2...3...4...
 000000D0 : 35 00 00 00 36 00 00 00 37 00 00 00 38 00 00 00   5...6...7...8...
 000000E0 : 39 00 00 00 3A 00 00 00 3B 00 00 00 3C 00 00 00   9...:...;...<...
 000000F0 : 3D 00 00 00 3F 00 00 00 51 00 00 00 40 00 00 00   =...?...Q...@...
 00000100 : 41 00 00 00 42 00 00 00 43 00 00 00 44 00 00 00   A...B...C...D...
 00000110 : 45 00 00 00 46 00 00 00 47 00 00 00 48 00 00 00   E...F...G...H...
 00000120 : 49 00 00 00 4A 00 00 00 4B 00 00 00 4C 00 00 00   I...J...K...L...
 00000130 : 4D 00 00 00 4E 00 00 00 4F 00 00 00 50 00 00 00   M...N...O...P...
 00000140 : 52 00 00 00 FE FF FF FF 22 03 00 00 FD FF FF FF   R.......".......
 00000150 : FD FF FF FF 56 00 00 00 57 00 00 00 58 00 00 00   ....V...W...X...
 00000160 : 59 00 00 00 5A 00 00 00 5B 00 00 00 5C 00 00 00   Y...Z...[...\...
 00000170 : 5D 00 00 00 5E 00 00 00 5F 00 00 00 60 00 00 00   ]...^..._...`...
 00000180 : 61 00 00 00 62 00 00 00 63 00 00 00 64 00 00 00   a...b...c...d...
 00000190 : 65 00 00 00 66 00 00 00 67 00 00 00 68 00 00 00   e...f...g...h...
 000001A0 : 69 00 00 00 6A 00 00 00 6B 00 00 00 6C 00 00 00   i...j...k...l...
 000001B0 : 6D 00 00 00 6E 00 00 00 6F 00 00 00 70 00 00 00   m...n...o...p...
 000001C0 : 71 00 00 00 72 00 00 00 73 00 00 00 74 00 00 00   q...r...s...t...
 000001D0 : 75 00 00 00 76 00 00 00 77 00 00 00 78 00 00 00   u...v...w...x...
 000001E0 : 79 00 00 00 7A 00 00 00 7B 00 00 00 7C 00 00 00   y...z...{...|...
 000001F0 : 7D 00 00 00 7E 00 00 00 7F 00 00 00 80 00 00 00   }...~...........
 ```
 
 4byte씩 끊어 읽으면 의미가 있다., First directory sector location 값이 2
 
 4byte단위로 첫 번째 부터 Entry 0 -> Entry 2부터 시작
 Entry 2 값 : 0x4    
 Entry 4 값 : 0x5  
 Entry 5 값 : 0x6  
 Entry 6 값 : 0x18   
 Entry 24 값 : 0xfffffffe    <- 끝!  
 
 완성된 chain
 Entry 2 -> Entry 4 -> Entry 5 -> Entry 6 -> Entry 24  
 이 순서대로 블록을 읽어 합치면 하나의 스트림이 완성
 
 #### Entry 값 설명
 0xFFFFFFFD ( -3 ) : 특수한 블록을 의미  
 0xFFFFFFFE ( -2 ) : chain의 끝을 의미  
 0xFFFFFFFF ( - 1 ) : 사용하지 않는 블록을 의미  
 
 ### 주요 항목
 각 블록에는 최대 4개의 property가 있다.  
 1개의 property 정보는 0x80크기로 구성
 
 #### 
