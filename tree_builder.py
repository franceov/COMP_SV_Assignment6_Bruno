# tree_builder.py
# Company directory using a simple binary tree structure.
# Implements EmployeeNode, TeamTree with recursive insert and print_tree,
# plus a small CLI program (company_directory) to interact with the tree.

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class EmployeeNode:
    """Represents a single employee in the team tree."""
    name: str
    left: Optional['EmployeeNode'] = None
    right: Optional['EmployeeNode'] = None

    def __repr__(self) -> str:
        l = self.left.name if self.left else None
        r = self.right.name if self.right else None
        return f"EmployeeNode(name={self.name!r}, left={l!r}, right={r!r})"


class TeamTree:
    """Manages the overall reporting structure (binary tree)."""

    def __init__(self) -> None:
        self.root: Optional[EmployeeNode] = None

    def insert(
        self,
        manager_name: str,
        employee_name: str,
        side: str,
        current_node: Optional[EmployeeNode] = None
    ) -> bool:
        """Recursive insertion of an employee under a manager."""
        if side is None:
            print("❌ Error: side must be 'left' or 'right'.")
            return False

        side_norm = side.strip().lower()
        if side_norm not in ("left", "right"):
            print("❌ Error: side must be 'left' or 'right'.")
            return False

        if self.root is None:
            print("❌ Error: Cannot insert because the team lead (root) is not set yet.")
            return False

        if current_node is None:
            current_node = self.root

        # Found the manager
        if current_node.name == manager_name:
            target_child = getattr(current_node, side_norm)
            if target_child is not None:
                print(f"❌ Error: {manager_name}'s {side_norm.upper()} side is already occupied by {target_child.name}.")
                return False
            setattr(current_node, side_norm, EmployeeNode(employee_name))
            return True

        # Search left
        if current_node.left is not None:
            if self.insert(manager_name, employee_name, side_norm, current_node.left):
                return True

        # Search right
        if current_node.right is not None:
            if self.insert(manager_name, employee_name, side_norm, current_node.right):
                return True

        if current_node is self.root:
            print(f"❌ Error: Manager named '{manager_name}' does not exist in the current team tree.")
        return False

    def print_tree(self, node: Optional[EmployeeNode] = None, level: int = 0) -> None:
        """Recursively prints the team structure."""
        if node is None:
            if level == 0:
                if self.root is None:
                    print("(empty team)")
                    return
                node = self.root
            else:
                return

        indent = "  " * level
        print(f"{indent}- {node.name}")
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)


def company_directory() -> None:
    """Interactive CLI for managing the team tree."""
    tree = TeamTree()

    MENU = """
📋 Team Management Menu
1. Add Team Lead (root)
2. Add Employee
3. Print Team Structure
4. Exit
"""
    while True:
        try:
            print(MENU)
            choice = input("Choose an option (1–4): ").strip()
            if choice == "1":
                name = input("Enter team lead's name: ").strip()
                if not name:
                    print("❌ Name cannot be empty.")
                    continue
                if tree.root is not None:
                    confirm = input("A team lead already exists. Replace it? (y/N): ").strip().lower()
                    if confirm != "y":
                        continue
                tree.root = EmployeeNode(name)
                print(f"✅ {name} added as the team lead.")
            elif choice == "2":
                if tree.root is None:
                    print("❌ Please add a team lead first (option 1).")
                    continue
                manager = input("Enter the manager's name: ").strip()
                employee = input("Enter the new employee's name: ").strip()
                side = input("Should this employee be on the LEFT or RIGHT of the manager? ").strip().lower()
                success = tree.insert(manager, employee, side)
                if success:
                    print(f"✅ {employee} added to the {side.upper()} of {manager}")
            elif choice == "3":
                print("\n🌳 Current Team Structure:")
                tree.print_tree()
                print()
            elif choice == "4":
                print("Good Bye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number 1–4.")
        except (KeyboardInterrupt, EOFError):
            print("\nGood Bye!")
            break


if __name__ == "__main__":
    company_directory()


"""
--- Design Memo (200–300 words) ---

Recursive insertion works by breaking the search problem into smaller subproblems.
Given a target manager’s name, we start at the root: if the current node matches
the manager, we check the requested side (left or right). If that side is empty,
we create a new EmployeeNode there; if it’s already occupied, we report an error.
If the current node is not the manager, we recursively search its left subtree,
and if not found, its right subtree. Each recursive call reduces the search
space until either we find the manager or we exhaust the tree. The function
returns True/False to signal success up the call stack so we can stop as soon
as we insert successfully.

The main challenge was ensuring we only print helpful error messages once and
avoid noisy output during deep recursion (e.g., “manager not found” repeated
many times). I handled this by only printing the “manager not found” message at
the top-level call (when current_node is the root), while lower-level calls
silently return False. Another common pitfall is normalizing user input for the
side (LEFT/RIGHT vs left/right); I standardized by lowercasing and validating.

Trees are preferable when hierarchical relationships must be represented
clearly and traversed efficiently. Examples include org charts, file systems,
dependency trees, and decision trees. Compared to linear structures (lists),
trees let us organize data by parent/child relationships and support recursive
operations (search/insert/print) that mirror real-world hierarchies. Compared
to hash maps, trees naturally preserve structure and ordering and can support
ordered traversals or proximity queries (e.g., nearest ancestor/descendant).
"""
