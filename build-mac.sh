#!/bin/bash
pyinstaller -F --onefile --noconsole --add-data "jambrl.xsl:." --osx-bundle-identifier com.chikim.ChartMaker ChartMaker.py
