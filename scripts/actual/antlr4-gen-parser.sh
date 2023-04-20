#!/bin/bash

ANTLR4_JAR=/usr/share/java/antlr-4.12.0-complete.jar

# java -jar ${ANTLR4_JAR} -Dlanguage=Python3 "$@"

java -Xmx500M -cp "${ANTLR4_JAR}:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python3 "$@"

