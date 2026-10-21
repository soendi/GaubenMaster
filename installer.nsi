; GaubenMaster NSIS Installer Script
; Erstellt einen Windows Installer mit Silent-Update-Unterstützung

!include "MUI2.nsh"
!include "x64.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; === Grundkonfiguration ===
Name "GaubenMaster"
OutFile "GaubenMaster-Setup-${PRODUCT_VERSION}.exe"
InstallDir "$LOCALAPPDATA\GaubenMaster"
InstallDirRegKey HKCU "Software\GaubenMaster" "InstallDir"

RequestExecutionLevel user
ShowInstDetails show
ShowUninstDetails show

; === Version ===
!define PRODUCT_PUBLISHER "soendi"
!define PRODUCT_WEB_SITE "https://github.com/soendi/GaubenMaster"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\GaubenMaster"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\GaubenMaster"
!define PRODUCT_UNINST_ROOT_KEY "HKCU"

; === MUI Settings ===
!define MUI_ABORTWARNING
!define MUI_ICON "assets/icon.ico"
!define MUI_UNICON "assets/icon.ico"

; Kein Wizard-Bitmap (Datei nicht vorhanden) - Standard MUI verwenden
!define MUI_WELCOMEPAGE_TITLE "Willkommen zum GaubenMaster Setup"
!define MUI_WELCOMEPAGE_TEXT "Dieser Assistent installiert GaubenMaster ${PRODUCT_VERSION} auf Ihrem Computer.\n\nKlicken Sie auf Weiter, um fortzufahren."

!define MUI_FINISHPAGE_TITLE "Installation abgeschlossen"
!define MUI_FINISHPAGE_TEXT "GaubenMaster ${PRODUCT_VERSION} wurde erfolgreich installiert.\n\nKlicken Sie auf Fertigstellen, um den Assistenten zu beenden."
!define MUI_FINISHPAGE_RUN "GaubenMaster.exe"
!define MUI_FINISHPAGE_RUN_TEXT "GaubenMaster starten"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "German"

; === Variablen ===
Var StartMenuFolder
Var PreviousInstallDir

; === Funktionen ===
Function .onInit
    ; Prüfen ob schon eine Version installiert ist
    ReadRegStr $PreviousInstallDir HKCU "${PRODUCT_UNINST_KEY}" "InstallDir"
    StrCmp $PreviousInstallDir "" 0 +2
    ReadRegStr $PreviousInstallDir HKLM "${PRODUCT_UNINST_KEY}" "InstallDir"
    
    ; Silent Install Detection
    ${GetParameters} $R0
    ${GetOptions} $R0 "/SILENT" $R1
    StrCmp $R1 "" NotSilent
    ; Silent Install - keine UI
    StrCpy $INSTDIR "$LOCALAPPDATA\GaubenMaster"
    Call SilentInstall
    Quit
NotSilent:
FunctionEnd

Function SilentInstall
    ; Silent Installation ohne UI
    CreateDirectory $INSTDIR
    SetOutPath $INSTDIR
    
    ; Dateien kopieren
    File "dist\GaubenMaster.exe"
    
    ; Uninstaller erstellen
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Registry Einträge für Uninstall
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName" "GaubenMaster"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "QuietUninstallString" "$INSTDIR\uninstall.exe /SILENT"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "InstallDir" $INSTDIR
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "NoModify" "1"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "NoRepair" "1"
    WriteRegDWORD HKCU "${PRODUCT_UNINST_KEY}" "EstimatedSize" 50000
    
    ; Startmenü Verknüpfung
    CreateDirectory "$SMPROGRAMS\GaubenMaster"
    CreateShortCut "$SMPROGRAMS\GaubenMaster\GaubenMaster.lnk" "$INSTDIR\GaubenMaster.exe"
    CreateShortCut "$SMPROGRAMS\GaubenMaster\Deinstallieren.lnk" "$INSTDIR\uninstall.exe"
    
    ; Desktop Verknüpfung
    CreateShortCut "$DESKTOP\GaubenMaster.lnk" "$INSTDIR\GaubenMaster.exe"
    
    ; InstallDir speichern
    WriteRegStr HKCU "Software\GaubenMaster" "InstallDir" $INSTDIR
    WriteRegStr HKCU "Software\GaubenMaster" "Version" "${PRODUCT_VERSION}"
FunctionEnd

Function .onInstSuccess
    ; Nach erfolgreicher Installation
    WriteRegStr HKCU "Software\GaubenMaster" "InstallDir" $INSTDIR
    WriteRegStr HKCU "Software\GaubenMaster" "Version" "${PRODUCT_VERSION}"
FunctionEnd

; === Sektionen ===
Section "MainSection" SEC01
    SetOutPath $INSTDIR
    
    ; Hauptprogramm
    File "dist\GaubenMaster.exe"
    
    ; Uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Registry
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName" "GaubenMaster"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "QuietUninstallString" "$INSTDIR\uninstall.exe /SILENT"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "InstallDir" $INSTDIR
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "NoModify" "1"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "NoRepair" "1"
    WriteRegDWORD HKCU "${PRODUCT_UNINST_KEY}" "EstimatedSize" 50000
    
    ; Startmenü
    CreateDirectory "$SMPROGRAMS\GaubenMaster"
    CreateShortCut "$SMPROGRAMS\GaubenMaster\GaubenMaster.lnk" "$INSTDIR\GaubenMaster.exe" "" "" 0
    CreateShortCut "$SMPROGRAMS\GaubenMaster\Deinstallieren.lnk" "$INSTDIR\uninstall.exe" "" "" 0
    
    ; Desktop
    CreateShortCut "$DESKTOP\GaubenMaster.lnk" "$INSTDIR\GaubenMaster.exe" "" "" 0
    
    ; InstallDir speichern
    WriteRegStr HKCU "Software\GaubenMaster" "InstallDir" $INSTDIR
    WriteRegStr HKCU "Software\GaubenMaster" "Version" "${PRODUCT_VERSION}"
SectionEnd

; === Deinstallation ===
Section "Uninstall"
    ; Dateien löschen
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"
    
    ; Shortcuts löschen
    Delete "$SMPROGRAMS\GaubenMaster\*.*"
    RMDir "$SMPROGRAMS\GaubenMaster"
    Delete "$DESKTOP\GaubenMaster.lnk"
    
    ; Registry löschen
    DeleteRegKey HKCU "${PRODUCT_UNINST_KEY}"
    DeleteRegKey HKCU "Software\GaubenMaster"
    
    ; Leere Verzeichnisse entfernen
    RMDir "$INSTDIR"
SectionEnd

; === Silent Uninstall ===
Function un.onInit
    ${GetParameters} $R0
    ${GetOptions} $R0 "/SILENT" $R1
    StrCmp $R1 "" NotSilentUninstall
    ; Silent Uninstall
    Push "Silent"
    Call un.UninstallSilent
    Quit
NotSilentUninstall:
FunctionEnd

Function un.UninstallSilent
    Pop $R0
    ; Dateien löschen
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"
    
    ; Shortcuts löschen
    Delete "$SMPROGRAMS\GaubenMaster\*.*"
    RMDir "$SMPROGRAMS\GaubenMaster"
    Delete "$DESKTOP\GaubenMaster.lnk"
    
    ; Registry löschen
    DeleteRegKey HKCU "${PRODUCT_UNINST_KEY}"
    DeleteRegKey HKCU "Software\GaubenMaster"
FunctionEnd

; === Custom Functions für Silent Update ===
; Diese Funktionen werden vom Auto-Update aufgerufen:
; GaubenMaster-Setup-<version>.exe /SILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS

; /CLOSEAPPLICATIONS - Schließt laufende Instanzen
; /RESTARTAPPLICATIONS - Startet die App nach Installation neu
; /NORESTART - Kein Windows-Neustart
; /SUPPRESSMSGBOXES - Keine Messageboxen
; /SILENT - Keine UI

; Der Installer erkennt diese Parameter automatisch über die .onInit Funktion