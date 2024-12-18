import click
import os
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from .helpers import check_path_or_url,find_section_indices
import datetime

console = Console()


@click.group()
def cli():
    pass

@cli.command('post')
@click.option('--path',"-p", default=os.path.join("~","TEXTBLOG.MD"))
@click.argument('username')
@click.option("--title","-t", prompt="Enter the blog post title")
def add_blog_post(path, username,title):
    # Check if the file exists
    if not os.path.exists(path):
        # Create the file and write the header
        with open(path, 'w') as file:
            file.write(f"#  {username}'s blog\n")
            file.write("# Followed blogs\n")
    else:
        # Open the file in read mode
        with open(path, 'r') as file:
            content = file.readlines()

        # Find the index of the last line in the blog section
        blog_section_end = next((i for i, line in reversed(list(enumerate(content))) if line.startswith("#  ")), -1)

        post_content = Prompt.ask("Enter the blog post content")

        # Append the new blog post after the last line in the blog section
        new_post = f"## {title}\n##  {datetime.datetime.now().isoformat()}\n{post_content}\n"
        content.insert(blog_section_end, new_post)

        # Convert the list of strings into a single string
        updated_content = ''.join(content)

        # Write the updated content back to the file
        with open(path, 'w') as file:
            file.write(updated_content)


@cli.command('follow')
@click.option('--path',"-p", default=os.path.join("~","TEXTBLOG.MD"))
@click.option("--url", prompt='Enter the URL of the blog to follow')
@click.option("--username", "-u", prompt="Enter the username of the blogger to follow")
def follow_blog(path, url, username):
    with open(path, 'r+') as file:
        content = file.readlines()

    start_index, end_index = find_section_indices(content, "#Followed blogs")
    if start_index is None:
        console.print("Section '#Followed blogs' not found.")
        return

    followed_blogs = content[start_index:end_index]
    followed_blogs.append(f"[{username}]({url})\n")

    confirm = Confirm.ask(f"Confirm subscription to {username}@{url}?")
    if confirm:
        with open(path, 'w+') as file:
            file.writelines(content[:start_index] + followed_blogs + content[end_index:])
        console.print(f"Successfully followed {username}.")
    else:
        console.print("Subscription canceled.")


@cli.command("read")
@click.argument("blog_path")
def read_blog(blog_path):
    path_or_url = check_path_or_url(blog_path)
    if path_or_url[0] == "path":
        if path_or_url[1] is True:
            with open(blog_path, "r") as blog:
                content = blog.read()
            md = Markdown(content)
            console.print(md)
        else:
            console.print("Blog invalid")
    elif path_or_url[0] == "url":
        r = requests.get(blog_path)
        if r.status_code == 200:
            console.print("Blog Found!")
            content = r.content
            md = Markdown(content)
            console.print(md)
        else:
            console.print("Blog invalid")
    else:
        console.print("Blog invalid")


if __name__ == "__main__":
    cli()