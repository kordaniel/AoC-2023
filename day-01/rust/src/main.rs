struct Input {
    lines: Vec<String>,
}

mod helpers {
    use std::env;
    use std::fs;
    use std::process;

    use super::Input;

    pub fn parse_args() -> String {
        let args: Vec<String> = env::args().collect();

        if args.len() != 2 {
            eprintln!("Invalid arguments. Please pass the path of the input file as the only arg");
            process::exit(1);
        }

        args[1].clone()
    }

    pub fn read_input(fpath: &str) -> Input {
        let lines = fs::read_to_string(fpath)
            .unwrap() // panic on possible file-reading errors
            .lines() // split the string into an iterator of string slices
            .map(String::from) // Make each slice into a string
            .collect(); // gather all the slices into a vector

            Input { lines }
    }
}

mod problem1 {
    use super::Input;

    /// Parses the first and last digits in the line, concatenates them into
    /// one i32 value and returns the result.
    ///
    /// Note: If the string contains no digits, returns 0
    ///       If the string contains only one digit, returns that digit concatenated into itself
    fn process_line(line: &str) -> i32 {
        let mut chars = String::new();

        for c in line.chars() {
            if c.is_digit(10) {
                chars.push(c);
            }
        }

        match chars.chars().count() {
            0 => 0,
            1 => chars
                    .chars()
                    .flat_map(|c| std::iter::repeat(c).take(2))
                    .collect::<String>()
                    .parse::<i32>()
                    .unwrap_or(0),
            _ => {
                let numstr = format!(
                    "{}{}",
                    chars.chars().nth(0).unwrap(),
                    chars.chars().rev().nth(0).unwrap()
                );
                numstr.parse::<i32>().unwrap_or(0)
            },
        }
    }

    /// Parses the first and last digit of every line in the input, concatenates them into
    /// a value and returns the sum of all of the values.
    pub fn solve(inp: &Input) -> i32 {
        let mut nums: Vec<i32> = vec![];

        for line in inp.lines.iter() {
            nums.push(process_line(line));
        }

        nums.iter().sum::<i32>()
    }
}

mod problem2 {
    use std::collections::{HashMap, HashSet};
    use super::Input;

    fn generate_prefixes(nums: &HashMap<String, i32>) -> HashSet<String> {
        let mut prefixes: HashSet<String> = HashSet::new();
        let mut buff = String::new();

        for (numstr, _value) in nums {
            buff.clear();
            for c in numstr.chars() {
                buff.push(c);
                prefixes.insert(buff.clone());
            }
        }

        prefixes
    }

    fn parse_line(line: &str, nums: &HashMap<String, i32>, prefixes: &HashSet<String>) -> i32 {
        let mut l: usize = 0;
        let mut r: usize = 1;
        let mut numbers: Vec<i32> = Vec::new();

        while r <= line.len() {
            if nums.contains_key(&line[l..r]) {
                numbers.push(nums[&line[l..r]]);
                l = r;
                r = r+1;
                continue;
            }

            r -= 1;
            while r+1 <= line.len() && prefixes.contains(&line[l..(r+1)]) {
                r += 1;
            }

            if l == r {
                l += 1;
                r = l+1;
                continue;
            }

            let current = line[l..r].to_string();
            if nums.contains_key(&current) {
                numbers.push(nums[&current]);
            }

            l += 1;
            r = l+1;
        }

        // if there is only one number in the line, use the same number for both digits
        let first = numbers.iter().nth(0).unwrap();
        let last  = numbers.iter().rev().nth(0).unwrap();

        10*first + last
    }

    /// Parses the first and last number of every line in the input where each number can be
    /// a digit or a string representation of the number. Concatenates the first and last
    /// number of every line and finally returns a sum of all the concatenated values.
    ///
    /// Uses a very simple and slow straightforward algorithm which has been chosen
    /// with the objective of learning rust instead of focusing on performance.
    pub fn solve(inp: &Input) -> i32 {
        let nums: HashMap<String, i32> = HashMap::from([
            //("zero".to_string(),  0),
            ("one".to_string(),   1),
            ("two".to_string(),   2),
            ("three".to_string(), 3),
            ("four".to_string(),  4),
            ("five".to_string(),  5),
            ("six".to_string(),   6),
            ("seven".to_string(), 7),
            ("eight".to_string(), 8),
            ("nine".to_string(),  9),
            //("0".to_string(), 0),
            ("1".to_string(), 1),
            ("2".to_string(), 2),
            ("3".to_string(), 3),
            ("4".to_string(), 4),
            ("5".to_string(), 5),
            ("6".to_string(), 6),
            ("7".to_string(), 7),
            ("8".to_string(), 8),
            ("9".to_string(), 9),
        ]);
        let prefixes = generate_prefixes(&nums);
        let mut numbers: Vec<i32> = Vec::new();

        for line in inp.lines.iter() {
            numbers.push(parse_line(line, &nums, &prefixes));
        }

        numbers.iter().sum::<i32>()
    }
}

fn main() {
    let fpath = helpers::parse_args();
    let inp = helpers::read_input(&fpath);
    //let inp = Input {
    //    lines: vec![
    //        String::from("1abc2"),
    //        String::from("pqr3stu8vwx"),
    //        String::from("a1b2c3d4e5f"),
    //        String::from("treb7uchet"),
    //    ],
    //}; // = prob1: 142

    //let inp = Input {
    //    lines: vec![
    //        String::from("two1nine"),
    //        String::from("eightwothree"),
    //        String::from("abcone2threexyz"),
    //        String::from("xtwone3four"),
    //        String::from("4nineeightseven2"),
    //        String::from("zoneight234"),
    //        String::from("7pqrstsixteen"),
    //    ],
    //}; // = prob2: 281
    println!("Problem 1: {}", problem1::solve(&inp));
    println!("Problem 2: {}", problem2::solve(&inp));
}
