# MeshMill 출시

릴리스 파이프라인은 GitHub 호스팅 Windows 실행기에서 Windows 아티팩트를 빌드합니다. 최종 사용자는
독립형 설치 프로그램 또는 휴대용 ZIP을 사용하고 Python, Node.js 또는 종속 항목을 설치하지 마세요.

빌드하기 전에 현지화 소스 카탈로그를 새로 고치고 검증하십시오.

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## 첫 공개 전

1. 계획된 애플리케이션 및 문서 번역을 완료하고 검증합니다.
2. GPL 및 제3자 고지 사항을 검토하세요.
3. 깨끗한 환경에서 설치, 실행, STL 로딩, 최적화, 내보내기 및 제거를 테스트합니다.
   Windows 계정 또는 가상 머신.
4. `samples/sample-scan.stl`에 대해 CI를 실행합니다. 모든 문서 스크린샷을 검사하고 잘라냅니다.
   작업 표시줄, MeshMill의 일부가 아닌 창 크롬, 알림, 개인 경로, 계정
   게시하기 전에 세부 정보 및 관련 없는 데스크톱 콘텐츠를 확인하세요.
5. 이전에 계정의 GitHub 무응답 주소로 저장소-로컬 Git 작성자를 구성하십시오.
   첫 번째 커밋. `git config --local --get user.email`로 확인하세요.
6. 선택적 Authenticode 서명 비밀을 구성합니다.
   - `WINDOWS_CERTIFICATE_BASE64`: Base64로 인코딩된 PFX 인증서.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX 비밀번호.

서명 인증서가 없으면 생성된 파일은 계속 작동하지만 Windows SmartScreen에는 다음이 표시될 수 있습니다.
인식할 수 없는 게시자 경고입니다. 서명되지 않은 빌드를 서명되었거나 신뢰할 수 있는 것으로 설명하지 마십시오.

## 원본 스캔 및 Git LFS

`samples/original-scan.stl`는 GitHub의 일반 100MiB를 초과하므로 Git LFS를 통해 추적됩니다.
파일 제한. 첫 번째 커밋 전에 다음을 확인하세요.

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

필터는 `lfs`여야 하며 포인터 개체 ID는 `samples/SHA256SUMS.txt`와 일치해야 합니다. 릴리스
워크플로우는 LFS 컨텐츠를 체크아웃하고 원본 STL를 별도의 릴리스 자산으로 게시합니다. CI 용도
더 작은 일반 Git 샘플이며 LFS 개체를 다운로드하지 않습니다.

## 게시하지 않고 릴리스 빌드 테스트

**작업**을 열고 **릴리스**를 선택한 다음 **워크플로 실행**을 선택하고 다음과 같은 숫자 버전을 입력합니다.
`0.1.0`. 수동 실행은 테스트용 워크플로 아티팩트를 업로드하지만 공개 GitHub를 생성하지 않습니다.
릴리스.

## 릴리스 게시

깨끗하고 검토된 `main` 지점에서:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

태그는 출시 워크플로를 시작합니다. 그것:

1. 고정된 빌드 종속성을 설치합니다.
2. 일치하는 Windows 버전 메타데이터를 생성합니다.
3. 자체 포함된 GUI 및 CLI 실행 파일을 빌드합니다.
4. 서명 비밀이 구성되면 실행 파일에 서명합니다.
5. 사용자별 Inno Setup 설치 프로그램을 빌드합니다.
6. 구성되면 설치 프로그램에 서명합니다.
7. 휴대용 ZIP 및 SHA-256 체크섬 파일을 생성합니다.
8. 워크플로 아티팩트를 업로드합니다.
9. 푸시된 태그에 대한 GitHub 릴리스를 생성합니다.

릴리스를 발표하기 전에 깨끗한 Windows 시스템에서 설치 프로그램과 휴대용 아카이브를 확인하십시오.
동일한 릴리스 태그에서 사용 가능한 모든 배포 바이너리에 해당하는 소스를 유지하세요.
첫 번째 태그를 지정하기 전에 GitHub 버튼이 최종 공개 저장소 URL을 가리키는지 확인하세요.
릴리스.
