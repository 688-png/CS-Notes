#Git
<!-- GFM-TOC -->
* [Git](#git)
    * [Centralized vs. Distributed](#centralized vs. distributed)
    * [Central Server](#centerserver)
    * [workflow](#workflow)
    * [branch implementation](#branch implementation)
    * [conflict](#conflict)
    * [Fast forward](#fast-forward)
    * [Stashing](#storagestashing)
    * [SSH transfer settings](#ssh-transfer settings)
    * [.gitignore file](#gitignore-file)
    * [Git command list](#git-command list)
    * [References](#references)
<!-- GFM-TOC -->


## Centralized and distributed

Git is a distributed version control system, while SVN is centralized.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200656794.png"/> </div><br>

In centralized version control, only the central server has a copy of the code, while in distributed version control, everyone has a complete copy of the code on their computer.

Centralized version control has security issues. When the central server goes down, no one can work.

Centralized version control requires an Internet connection to work. If the Internet speed is too slow, submitting a file will be unbearably slow. Distributed version control does not require an Internet connection to work.

Distributed version control creates branches and merges branches very quickly, while creating a branch under centralized version control is equivalent to copying a complete code.

## Central server

The central server is used to exchange each user's modifications. It can work without a central server, but the central server can stay on 24 hours a day, so that modifications can be exchanged more conveniently.

Github is a central server.

## Workflow

After creating a new warehouse, the current directory becomes the workspace. There is a hidden directory .git under the workspace, which belongs to the Git repository.

Git's repository has a staging area called Stage and the final History repository. History stores all branch information and uses a HEAD pointer to point to the current branch.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208195941661.png"/> </div><br>

- git add files adds file modifications to the staging area
- git commit submits the changes in the temporary storage area to the current branch. After submission, the temporary storage area is cleared.
- git reset -- files overwrites the staging area with changes on the current branch, used to undo the last git add files
- git checkout -- files overwrites the working directory with changes in the staging area and is used to undo local changes.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200014395.png"/> </div><br>

You can skip the staging area and directly take the modifications from the branch, or directly submit the modifications to the branch.

- git commit -a directly adds all file modifications to the staging area and then executes the
commit
- git checkout HEAD -- files take out the last modification, which can be used for rollback operations

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208200543923.png"/> </div><br>

## Branch implementation

Use pointers to connect each commit into a timeline, with the HEAD pointer pointing to the current branch pointer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203219927.png"/> </div><br>

Creating a new branch means creating a new pointer pointing to the last node of the timeline, and letting the HEAD pointer point to the new branch, indicating that the new branch becomes the current branch.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203142527.png"/> </div><br>

Each commit will only move the current branch pointer forward, but other branch pointers will not move.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203112400.png"/> </div><br>

Merging branches only requires changing the pointer.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203010540.png"/> </div><br>

## Conflict

When two branches modify the same line of the same file, a conflict will occur when the branches are merged.

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/image-20191208203034705.png"/> </div><br>

Git will use \<\<\<\<\<\<\< , ======= , \>\>\>\>\>\>\> to mark the contents of different branches. You only need to modify the conflicting parts in different branches to be the same to resolve the conflict.

```
<<<<<<< HEAD
Creating a new branch is quick & simple.
=======
Creating a new branch is quick AND simple.
>>>>>>> feature1
```

## Fast forward

"Fast-farward merge" will directly point the master branch to the merged branch. Branch merging in this mode will lose branch information, so branch information cannot be seen in the branch history.

You can add the --no-ff parameter when merging to disable Fast forward mode, and add the -m parameter to generate a new commit when merging.

```
$ git merge --no-ff -m "merge with no-ff" dev
```

<div align="center"> <img src="https://cs-notes-125610979
6.cos.ap-guangzhou.myqcloud.com/image-20191208203639712.png"/> </div><br>

## Stashing

After working on one branch, if the modifications have not been submitted to the branch and you switch branches at this time, the new modifications will also be visible on the other branch. This is because all branches share a workspace.

You can use git stash to store the modifications of the current branch. At this time, all modifications in the current workspace will be stored in the stack, which means that the current workspace is clean and does not have any uncommitted modifications. At this point you can safely switch to other branches.

```
$ git stash
Saved working directory and index state \ "WIP on master: 049d078 added the index file"
HEAD is now at 049d078 added the index file (To restore them type "git stash apply")
```

This feature can be used for bug branch implementation. If you are currently developing on the dev branch, but there is a bug on the master that needs to be fixed, but the development on the dev branch has not been completed yet, and you do not want to submit it immediately. Before creating a new bug branch and switching to the bug branch, you need to use git stash to store the uncommitted changes of the dev branch.

## SSH transfer settings

Transfers between Git repositories and Github central repositories are encrypted via SSH.

If there is no .ssh directory in the workspace, or there are no id_rsa and id_rsa.pub files in the directory, you can create an SSH Key with the following command:

```
$ ssh-keygen -t rsa -C "youremail@example.com"
```

Then copy the contents of the public key id_rsa.pub to SSH Keys in Github "Account settings".

## .gitignore file

Ignore the following files:

- Files automatically generated by the operating system, such as thumbnails;
- Intermediate files generated by compilation, such as .class files generated by Java compilation;
- Your own sensitive information, such as configuration files that store passwords.

You don’t need to write everything yourself, you can go to [https://github.com/github/gitignore](https://github.com/github/gitignore) to query.

## Git command list

<div align="center"> <img src="https://cs-notes-1256109796.cos.ap-guangzhou.myqcloud.com/7a29acce-f243-4914-9f00-f2988c528412.jpg" width=""> </div><br>

More detailed address: http://www.cheat-sheets.org/saved-copy/git-cheat-sheet.pdf

## References

- [Git - A Concise Guide](http://rogerdudler.github.io/git-guide/index.zh.html)
- [Illustrated Git](http://marklodato.github.io/visual-git-guide/index-zh-cn.html)
- [Liao Xuefeng: Git Tutorial](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
- [Learn Git Branching](https://learngitbranching.js.org/)
