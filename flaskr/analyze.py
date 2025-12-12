import os
from ollama import Client
from dotenv import load_dotenv


load_dotenv()


def analyze(code: str):
    client = Client(
        host="https://ollama.com",
        headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")},
    )

    messages = [
        {
            "role": "user",
            "content": f"Can you take on the role of a senior front end engineer and help me with refactoring the following code for testability. If you see any noticeable issues within the code snipped shared, do point out the issues with suggestions for a cleaner, more scalable approach. D.R.Y., S.O.C. patterns should be taken into accountdo not over abstract it, think that more junior people should also be able to read it.also take into consideration refactoring the code in a way that it is easier then to test:\n\n{code}",
        },
    ]

    try:
        # Get streaming response
        stream = client.chat(model="gpt-oss:120b", messages=messages, stream=True)

        for chunk in stream:

            chunk_content = chunk.message.content

            yield chunk_content

    except Exception as e:
        return f"Error calling Ollama API: {str(e)}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="File refactor",
        description="Suggest code refactor using Ollama API",
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=[".tsx", ".jsx"],
        help="File extensions to include (e.g. .tsx .jsx)",
    )
    parser.add_argument(
        "-ignored",
        "--ignored_directories",
        nargs="+",
        default=["node_modules", "__tests__", "dist", "build"],
        help="Directories to ignore (e.g. .git node_modules)",
    )

    args = parser.parse_args()
    exts = tuple(args.extensions)
    ignored_dirs = tuple(args.ignored_directories)

    from find_files import find_files_in_dir

    found = list(
        find_files_in_dir(
            args.path, file_extensions=exts, ignored_directories=ignored_dirs
        )
    )

    found = dict(enumerate(found, 1))
    length = len(found)
    print(f"Found {length} JS files in path {args.path}")

    if length == 0:
        print(f"No JS files found in path {args.path}")
        exit()

    print(f"Found {length} JS files in path {args.path}")

    for key, value in found.items():
        print(f"{key}: {value}")

    user_choice = int(
        input(
            f">>>> Which file would you like to analyze with AI? Chose one between 1 and {length}:\n"
        )
    )
    chosen_file = found[user_choice]

    content = ""

    with open(chosen_file, "r") as f:
        content = f.read()

    for chunk in analyze(content):
        print(chunk, end="", flush=True)
