cmake_minimum_required(VERSION 3.10)
project(calculation_lib_project LANGUAGES C)

#динамическая
add_library(calculation SHARED c_src/calculation.c)

target_include_directories(calculation PUBLIC c_src)

set_target_properties(calculation PROPERTIES C_VISIBILITY_PRESET default)

install(TARGETS calculation DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/lib)
