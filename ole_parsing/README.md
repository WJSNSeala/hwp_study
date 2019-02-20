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

#### 