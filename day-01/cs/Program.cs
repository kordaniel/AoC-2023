// See https://aka.ms/new-console-template for more information

using System;
using System.Collections.Generic;

string
ConcatenateFirstAndLastDigit(string line)
{
    char[] chars = {'\0', '\0'};
    int i;

    for (i = 0; i < line.Length; i++)
    {
        if (Char.IsDigit(line, i))
        {
            chars[0] = line[i];
            break;
        }
    }

    for (int j = line.Length-1; j >= i; j--)
    {
        if (char.IsDigit(line, j))
        {
            chars[1] = line[j];
            break;
        }
    }

    if (chars[0] == '\0' || chars[1] == '\0')
    {
        throw new ArgumentException("Invalid input line: Contains no digits.");
    }

    return new string(chars);
}

List<int>
GetCalibrationValues(List<string> lines) => lines
    .Select(ConcatenateFirstAndLastDigit)
    .Select(calibVal => int.Parse(calibVal))
    .ToList();


//string[] lines = {
//    "1abc2",
//    "pqr3stu8vwx",
//    "a1b2c3d4e5f",
//    "treb7uchet",
//};
//List<string> inp = new List<string>(lines);

List<string> inp = new List<string>(File.ReadAllLines("input.txt"));
List<int> calibVals = GetCalibrationValues(inp);
Console.WriteLine($"Part 1: {calibVals.Sum()}");
