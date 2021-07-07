#ifndef CODE_TEMPLATE
#define CODE_TEMPLATE

#define CXX_COMPILER_SIMPLETEST \
"#include <iostream>\n" \
"\n" \
"int main()\n" \
"{\n" \
"    std::cout << \"Hello world!\" << std::endl;\n" \
"    return 0;\n" \
"}"

#define NMake_SIMPLETEST \
"SRC = %sHelloWorld.cpp\n" \
"EXE = %sHelloWorld.exe\n" \
"OBJ = %s\\\n\n" \
"LINK_FLAG = \n" \
"CXX_FLAG = /EHsc\n" \
"$(EXE):\n" \
"	cl $(CXX_FLAG) $(SRC) /Fo$(OBJ) /link $(LINK_FLAG) kernel32.Lib /out:$(EXE)\n" \
"clean: \n" \
"	del *.obj\n" \
"	del *.exe"

#define MSBUILD_SIMPLETEST_VCXPROJ \
"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" \
"<Project DefaultTargets=\"Build\" ToolsVersion=\"12.0\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\">\n" \
"  <ItemGroup Label=\"ProjectConfigurations\">\n" \
"    <ProjectConfiguration Include=\"Debug|Win32\">\n" \
"      <Configuration>Debug</Configuration>\n" \
"      <Platform>Win32</Platform>\n" \
"    </ProjectConfiguration>\n" \
"    <ProjectConfiguration Include=\"Release|Win32\">\n" \
"      <Configuration>Release</Configuration>\n" \
"      <Platform>Win32</Platform>\n" \
"    </ProjectConfiguration>\n" \
"  </ItemGroup>\n" \
"  <PropertyGroup Label=\"Globals\">\n" \
"    <ProjectGuid>{40798B15-00BF-44DF-9FAB-56583AAAF2D2}</ProjectGuid>\n" \
"    <Keyword>Win32Proj</Keyword>\n" \
"    <RootNamespace>HelloWorld</RootNamespace>\n" \
"  </PropertyGroup>\n" \
"  <Import Project=\"$(VCTargetsPath)\\Microsoft.Cpp.Default.props\" />\n" \
"  <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Debug|Win32'\" Label=\"Configuration\">\n" \
"    <ConfigurationType>Application</ConfigurationType>\n" \
"    <UseDebugLibraries>true</UseDebugLibraries>\n" \
"    <PlatformToolset>v120</PlatformToolset>\n" \
"    <CharacterSet>Unicode</CharacterSet>\n" \
"  </PropertyGroup>\n" \
"  <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Release|Win32'\" Label=\"Configuration\">\n" \
"    <ConfigurationType>Application</ConfigurationType>\n" \
"    <UseDebugLibraries>false</UseDebugLibraries>\n" \
"    <PlatformToolset>v120</PlatformToolset>\n" \
"    <WholeProgramOptimization>true</WholeProgramOptimization>\n" \
"    <CharacterSet>Unicode</CharacterSet>\n" \
"  </PropertyGroup>\n" \
"  <Import Project=\"$(VCTargetsPath)\\Microsoft.Cpp.props\" />\n" \
"  <ImportGroup Label=\"ExtensionSettings\">\n" \
"  </ImportGroup>\n" \
"  <ImportGroup Label=\"PropertySheets\" Condition=\"'$(Configuration)|$(Platform)'=='Debug|Win32'\">\n" \
"    <Import Project=\"$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props\" Condition=\"exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')\" Label=\"LocalAppDataPlatform\" />\n" \
"  </ImportGroup>\n" \
"  <ImportGroup Label=\"PropertySheets\" Condition=\"'$(Configuration)|$(Platform)'=='Release|Win32'\">\n" \
"    <Import Project=\"$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props\" Condition=\"exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')\" Label=\"LocalAppDataPlatform\" />\n" \
"  </ImportGroup>\n" \
"  <PropertyGroup Label=\"UserMacros\" />\n" \
"  <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Debug|Win32'\">\n" \
"    <LinkIncremental>true</LinkIncremental>\n" \
"  </PropertyGroup>\n" \
"  <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Release|Win32'\">\n" \
"    <LinkIncremental>false</LinkIncremental>\n" \
"  </PropertyGroup>\n" \
"  <ItemDefinitionGroup Condition=\"'$(Configuration)|$(Platform)'=='Debug|Win32'\">\n" \
"    <ClCompile>\n" \
"      <PrecompiledHeader>\n" \
"      </PrecompiledHeader>\n" \
"      <WarningLevel>Level3</WarningLevel>\n" \
"      <Optimization>Disabled</Optimization>\n" \
"      <PreprocessorDefinitions>WIN32;_DEBUG;_CONSOLE;_LIB;%(PreprocessorDefinitions)</PreprocessorDefinitions>\n" \
"    </ClCompile>\n" \
"    <Link>\n" \
"      <SubSystem>Console</SubSystem>\n" \
"      <GenerateDebugInformation>true</GenerateDebugInformation>\n" \
"    </Link>\n" \
"  </ItemDefinitionGroup>\n" \
"  <ItemDefinitionGroup Condition=\"'$(Configuration)|$(Platform)'=='Release|Win32'\">\n" \
"    <ClCompile>\n" \
"      <WarningLevel>Level3</WarningLevel>\n" \
"      <PrecompiledHeader>\n" \
"      </PrecompiledHeader>\n" \
"      <Optimization>MaxSpeed</Optimization>\n" \
"      <FunctionLevelLinking>true</FunctionLevelLinking>\n" \
"      <IntrinsicFunctions>true</IntrinsicFunctions>\n" \
"      <PreprocessorDefinitions>WIN32;NDEBUG;_CONSOLE;_LIB;%(PreprocessorDefinitions)</PreprocessorDefinitions>\n" \
"    </ClCompile>\n" \
"    <Link>\n" \
"      <SubSystem>Console</SubSystem>\n" \
"      <GenerateDebugInformation>true</GenerateDebugInformation>\n" \
"      <EnableCOMDATFolding>true</EnableCOMDATFolding>\n" \
"      <OptimizeReferences>true</OptimizeReferences>\n" \
"    </Link>\n" \
"  </ItemDefinitionGroup>\n" \
"  <ItemGroup>\n" \
"    <ClCompile Include=\"HelloWorld.cpp\" />\n" \
"  </ItemGroup>\n" \
"  <Import Project=\"$(VCTargetsPath)\\Microsoft.Cpp.targets\" />\n" \
"  <ImportGroup Label=\"ExtensionTargets\">\n" \
"  </ImportGroup>\n" \
"</Project>"

#define MSBUILD_SIMPLETEST_SLN \
"Microsoft Visual Studio Solution File, Format Version 12.00\n" \
"# Visual Studio 2013\n" \
"VisualStudioVersion = 12.0.40629.0\n" \
"MinimumVisualStudioVersion = 10.0.40219.1\n" \
"Project(\"{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}\") = \"HelloWorld\", \"HelloWorld.vcxproj\", \"{40798B15-00BF-44DF-9FAB-56583AAAF2D2}\"\n" \
"EndProject\n" \
"Global\n" \
"	GlobalSection(SolutionConfigurationPlatforms) = preSolution\n" \
"		Debug|Win32 = Debug|Win32\n" \
"		Release|Win32 = Release|Win32\n" \
"	EndGlobalSection\n" \
"	GlobalSection(ProjectConfigurationPlatforms) = postSolution\n" \
"		{40798B15-00BF-44DF-9FAB-56583AAAF2D2}.Debug|Win32.ActiveCfg = Debug|Win32\n" \
"		{40798B15-00BF-44DF-9FAB-56583AAAF2D2}.Debug|Win32.Build.0 = Debug|Win32\n" \
"		{40798B15-00BF-44DF-9FAB-56583AAAF2D2}.Release|Win32.ActiveCfg = Release|Win32\n" \
"		{40798B15-00BF-44DF-9FAB-56583AAAF2D2}.Release|Win32.Build.0 = Release|Win32\n" \
"	EndGlobalSection\n" \
"	GlobalSection(SolutionProperties) = preSolution\n" \
"		HideSolutionNode = FALSE\n" \
"	EndGlobalSection\n" \
"EndGlobal"

#define CMAKE_SIMPLETEST \
"cmake_minimum_required(VERSION 2.8)\n" \
"project(HelloWorld)\n" \
"add_executable(HelloWorld HelloWorld.cpp)"

#endif // CODE_TEMPLATE