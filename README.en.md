# Config GUI Generator
Languages: [简体中文](./README.md) | English

Because I'm not good at English, you'd better read the Chinese version of README, which is always the latest and most accurate version.

## Description
> It's too boring to writing the ConfigWindow class and ConfigData class in GUI softwares. I want to be able to generate code automatically.

👆 Based on this idea, I developed this tool.

**Currently, only GUI code generation based on `Python3` + `PyQt5` is supported.**

Through this tool, you can declare the config data and its layout in a **HTML-like** format. The tool will automatically generate a template code containing ConfigWindow class and ConfigData class. The generated code can be used with just a little modification, which greatly reduces the workload of programmers.

- **Q** Why use `class` to store config data instead of `dict` ?
- **A** Using `class` allows IDE to help check spelling errors to avoid low-level errors.
- **Q** Why declare in HTML-like format instead of JSON format?
- **A** Reduce the difficulty of getting started, and enable programmers to preview the effect to a certain extent.