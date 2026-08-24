#define MyAppName "GladLang"
#define MyAppPublisher "Glad432"
#define MyAppExeName "gladlang.exe"

#define MyAppVersion GetEnv("GLADLANG_VERSION")
#define MyCopyrightYear GetDateTimeString("yyyy", "-", ":")

#if MyAppVersion == ""
  #error GLADLANG_VERSION environment variable is not set
#endif


[Setup]

AppId={{7AD3AA6C-5F5B-4B52-9C04-1188CDE1D3A4}}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\GladLang
DefaultGroupName=GladLang

PrivilegesRequired=lowest
Uninstallable=yes
ChangesEnvironment=yes
ChangesAssociations=yes

OutputDir=..\installer-output
OutputBaseFilename=GladLang-{#MyAppVersion}-Setup

SetupIconFile=..\favicon.ico

Compression=lzma
SolidCompression=yes
WizardStyle=modern

UninstallDisplayName=GladLang
UninstallDisplayIcon={app}\gladlang.exe

VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=GladLang Programming Language
VersionInfoProductName=GladLang
VersionInfoProductVersion={#MyAppVersion}.0
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright=Copyright (C) {#MyCopyrightYear} Glad432


[Files]

Source: "..\dist\gladlang.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]

Name: "{autoprograms}\GladLang"; \
    Filename: "{app}\gladlang.exe"; \
    IconFilename: "{app}\gladlang.exe"

Name: "{autodesktop}\GladLang"; \
    Filename: "{app}\gladlang.exe"; \
    IconFilename: "{app}\gladlang.exe"


[Tasks]

Name: "addtopath"; \
    Description: "Add GladLang to PATH"; \
    GroupDescription: "Additional options:"


[Registry]

Root: HKCU; \
    Subkey: "Environment"; \
    ValueType: expandsz; \
    ValueName: "Path"; \
    ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath(ExpandConstant('{app}')); \
    Flags: preservestringtype

Root: HKCU; \
    Subkey: "Software\Classes\.glad"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "GladLang.File"; \
    Flags: uninsdeletevalue

Root: HKCU; \
    Subkey: "Software\Classes\GladLang.File"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "GladLang Source File"; \
    Flags: uninsdeletekey

Root: HKCU; \
    Subkey: "Software\Classes\GladLang.File\DefaultIcon"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: "{app}\gladlang.exe,0"

Root: HKCU; \
    Subkey: "Software\Classes\GladLang.File\shell\open\command"; \
    ValueType: string; \
    ValueName: ""; \
    ValueData: """{app}\gladlang.exe"" ""%1"""


[Code]

procedure SHChangeNotify(wEventId: Integer; uFlags: Integer; dwItem1: Integer; dwItem2: Integer);
external 'SHChangeNotify@shell32.dll stdcall';

function NeedsAddPath(AppPath: string): Boolean;
var
  Paths: string;
  Entry: string;
  Remaining: string;
  NormalizedAppPath: string;
  NormalizedEntry: string;
  P: Integer;
begin
  if not WizardIsTaskSelected('addtopath') then
  begin
    Result := False;
    Exit;
  end;

  if not RegQueryStringValue(
    HKEY_CURRENT_USER,
    'Environment',
    'Path',
    Paths
  ) then
  begin
    Result := True;
    Exit;
  end;

  NormalizedAppPath := UpperCase(AppPath);

  while (Length(NormalizedAppPath) > 0) and
        (NormalizedAppPath[Length(NormalizedAppPath)] = '\') do
  begin
    Delete(
      NormalizedAppPath,
      Length(NormalizedAppPath),
      1
    );
  end;

  Remaining := Paths;

  while Remaining <> '' do
  begin
    P := Pos(';', Remaining);

    if P > 0 then
    begin
      Entry := Copy(Remaining, 1, P - 1);
      Delete(Remaining, 1, P);
    end
    else
    begin
      Entry := Remaining;
      Remaining := '';
    end;

    Entry := Trim(Entry);

    while (Length(Entry) > 0) and
          (Entry[Length(Entry)] = '\') do
    begin
      Delete(
        Entry,
        Length(Entry),
        1
      );
    end;

    NormalizedEntry := UpperCase(Entry);

    if NormalizedEntry = NormalizedAppPath then
    begin
      Result := False;
      Exit;
    end;
  end;

  Result := True;
end;


procedure RemoveGladLangFromPath(AppPath: string);
var
  Paths: string;
  Entry: string;
  Remaining: string;
  NewPath: string;
  NormalizedAppPath: string;
  NormalizedEntry: string;
  P: Integer;
begin
  if not RegQueryStringValue(
    HKEY_CURRENT_USER,
    'Environment',
    'Path',
    Paths
  ) then
    Exit;

  NormalizedAppPath := UpperCase(AppPath);

  while (Length(NormalizedAppPath) > 0) and
        (NormalizedAppPath[Length(NormalizedAppPath)] = '\') do
  begin
    Delete(
      NormalizedAppPath,
      Length(NormalizedAppPath),
      1
    );
  end;

  Remaining := Paths;
  NewPath := '';

  while Remaining <> '' do
  begin
    P := Pos(';', Remaining);

    if P > 0 then
    begin
      Entry := Copy(Remaining, 1, P - 1);
      Delete(Remaining, 1, P);
    end
    else
    begin
      Entry := Remaining;
      Remaining := '';
    end;

    Entry := Trim(Entry);

    NormalizedEntry := Entry;

    while (Length(NormalizedEntry) > 0) and
          (NormalizedEntry[Length(NormalizedEntry)] = '\') do
    begin
      Delete(
        NormalizedEntry,
        Length(NormalizedEntry),
        1
      );
    end;

    NormalizedEntry := UpperCase(NormalizedEntry);

    if NormalizedEntry <> NormalizedAppPath then
    begin
      if NewPath <> '' then
        NewPath := NewPath + ';';

      NewPath := NewPath + Entry;
    end;
  end;

  RegWriteStringValue(
    HKEY_CURRENT_USER,
    'Environment',
    'Path',
    NewPath
  );
end;


procedure CurUninstallStepChanged(
  CurUninstallStep: TUninstallStep
);
begin
  if CurUninstallStep = usUninstall then
  begin
    RemoveGladLangFromPath(
      ExpandConstant('{app}')
    );

    SHChangeNotify($08000000, $0000, 0, 0);
  end;
end;