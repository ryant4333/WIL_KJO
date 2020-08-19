# Archive
![alt text](archive.PNG)
___
## Attributes
* solution: LinkedList(Solution)
The solution attribute is a linked list of solution objects. This is because a linked list is the best data structure for inserting and deleting objects. Linked lists aren't so good for searching and indexing, however since the push operation is linear anyway this doesn't matter.
___
## Methods
* push(Solution): void
The push methods adds a solution to the archive. That solution will need to be compared to the other solutions to see if it fully dominates any of them.  
    * The first solution it finds that it can completely dominate, that solution is removed from the archive and the new dominate solution is added. 
    * If it finds one solution where the new solution is completely dominated, then it doesn't add the new solution. 
    * If the method has looked at all solutions and the other two cases didn't occur, the solution is added.

* output(): void
This will be used at the end of the program to output the best possible solutions that the program could find.
