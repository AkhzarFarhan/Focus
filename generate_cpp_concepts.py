#!/usr/bin/env python3
"""Generate comprehensive C/C++ concepts JSON for interview preparation."""
import json
import os

def chapter_pointers():
    return {
        "id": 1,
        "title": "Pointers Fundamentals",
        "slug": "pointers-fundamentals",
        "description": "Master raw pointers, pointer arithmetic, function pointers, and common pointer pitfalls in C/C++.",
        "icon": "🎯",
        "difficulty": "intermediate",
        "topics": [
            {
                "id": "1.1",
                "title": "Raw Pointers & Pointer Declaration",
                "explanation": "A pointer stores the memory address of another variable. The type of a pointer determines how the memory at that address is interpreted. Pointers are fundamental to C/C++ and are used for dynamic memory, data structures, and hardware interaction.\n\nDeclaration: `int *p;` declares a pointer to int. The `*` binds to the variable name, not the type, so `int *a, b;` declares a pointer `a` and an int `b`.",
                "keyPoints": [
                    "A pointer holds a memory address, not a value",
                    "The size of a pointer depends on the architecture (4 bytes on 32-bit, 8 bytes on 64-bit)",
                    "Dereferencing (*p) accesses the value at the address stored in p",
                    "The address-of operator (&) gives the address of a variable",
                    "Uninitialized pointers contain garbage addresses — always initialize to nullptr"
                ],
                "codeExamples": [
                    {
                        "title": "Basic Pointer Operations",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    int x = 42;\n    int *p = &x;       // p points to x\n\n    cout << \"Value of x: \" << x << endl;          // 42\n    cout << \"Address of x: \" << &x << endl;        // e.g., 0x7ffd5e8c\n    cout << \"Value of p: \" << p << endl;           // same address\n    cout << \"Dereferenced p: \" << *p << endl;      // 42\n\n    *p = 100;          // modify x through pointer\n    cout << \"x is now: \" << x << endl;             // 100\n\n    return 0;\n}",
                        "explanation": "Demonstrates declaration, address-of (&), dereferencing (*), and modifying a value through a pointer."
                    },
                    {
                        "title": "Pointer Size Across Types",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"sizeof(int*):    \" << sizeof(int*) << endl;    // 8 on 64-bit\n    cout << \"sizeof(char*):   \" << sizeof(char*) << endl;   // 8 on 64-bit\n    cout << \"sizeof(double*): \" << sizeof(double*) << endl; // 8 on 64-bit\n    cout << \"sizeof(void*):   \" << sizeof(void*) << endl;   // 8 on 64-bit\n    // All pointer sizes are the same on a given platform!\n    return 0;\n}",
                        "explanation": "All pointer types have the same size on a given platform — it's the address size, not the pointed-to type size."
                    }
                ],
                "commonMistakes": [
                    "Declaring int* a, b; thinking both are pointers (only a is a pointer)",
                    "Using uninitialized pointers (wild pointers) leading to undefined behavior",
                    "Confusing * in declaration (pointer type) vs * in expression (dereference)"
                ],
                "interviewTips": [
                    "Know the difference between pointer declaration and dereferencing",
                    "Be ready to explain why all pointer types have the same sizeof",
                    "Understand that pointers are just integers holding addresses"
                ]
            },
            {
                "id": "1.2",
                "title": "Pointer Arithmetic",
                "explanation": "Pointer arithmetic allows navigating memory by adding or subtracting integers from pointers. The key insight: when you add 1 to a pointer, it advances by sizeof(pointed_type) bytes, not 1 byte. This is why the type of a pointer matters.\n\nSubtracting two pointers of the same type gives the number of elements between them (ptrdiff_t).",
                "keyPoints": [
                    "p + n advances the pointer by n * sizeof(*p) bytes",
                    "Pointer subtraction (p2 - p1) gives the number of elements between two pointers",
                    "Pointer arithmetic is only defined within arrays or one-past-the-end",
                    "You can compare pointers with <, >, ==, != within the same array",
                    "Incrementing a char* moves by 1 byte; incrementing an int* moves by 4 bytes (typically)"
                ],
                "codeExamples": [
                    {
                        "title": "Pointer Arithmetic with Arrays",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    int arr[] = {10, 20, 30, 40, 50};\n    int *p = arr;  // points to arr[0]\n\n    cout << *p << endl;       // 10\n    cout << *(p + 1) << endl; // 20  (moved 4 bytes forward)\n    cout << *(p + 3) << endl; // 40\n\n    p += 2;  // now points to arr[2]\n    cout << *p << endl;       // 30\n\n    // Pointer difference\n    int *start = arr;\n    int *end = arr + 4;\n    cout << \"Elements between: \" << (end - start) << endl; // 4\n\n    // Array traversal using pointers\n    for (int *it = arr; it != arr + 5; ++it) {\n        cout << *it << \" \";\n    }\n    // Output: 10 20 30 40 50\n    return 0;\n}",
                        "explanation": "Shows how pointer arithmetic navigates arrays and that pointer difference gives element count, not byte count."
                    }
                ],
                "commonMistakes": [
                    "Assuming p+1 adds 1 byte (it adds sizeof(*p) bytes)",
                    "Performing arithmetic on void* (not allowed in C++, allowed as GCC extension in C)",
                    "Pointer arithmetic beyond array bounds is undefined behavior"
                ],
                "interviewTips": [
                    "Classic interview question: What does arr[i] actually mean? Answer: *(arr + i)",
                    "Know that arr[i] == i[arr] because both expand to *(arr + i)",
                    "Understand ptrdiff_t as the type for pointer differences"
                ]
            },
            {
                "id": "1.3",
                "title": "Pointer to Pointer & Void Pointers",
                "explanation": "A pointer to pointer (double pointer) stores the address of another pointer. This is used for modifying pointer values inside functions, 2D dynamic arrays, and argv in main().\n\nA void pointer (void*) is a generic pointer that can hold the address of any type but cannot be dereferenced directly — you must cast it first. It's the basis of C's generic programming (malloc returns void*).",
                "keyPoints": [
                    "int **pp declares a pointer to a pointer to int",
                    "Used in functions that need to modify a pointer argument",
                    "void* can hold any pointer type but cannot be dereferenced or used in arithmetic",
                    "C allows implicit void* conversion; C++ requires explicit cast",
                    "char **argv in main is a pointer to an array of char pointers"
                ],
                "codeExamples": [
                    {
                        "title": "Pointer to Pointer — Modifying a Pointer in a Function",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nvoid allocate(int **pp) {\n    *pp = new int(42);  // modifies the caller's pointer\n}\n\nint main() {\n    int *p = nullptr;\n    allocate(&p);       // pass address of the pointer\n    cout << *p << endl; // 42\n    delete p;\n    return 0;\n}",
                        "explanation": "Double pointer allows a function to allocate memory and update the caller's pointer. Without **, the function would only modify a local copy."
                    },
                    {
                        "title": "Void Pointer — Generic Swap",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <cstring>\nusing namespace std;\n\nvoid genericSwap(void *a, void *b, size_t size) {\n    char temp[256];  // buffer (use dynamic alloc for large sizes)\n    memcpy(temp, a, size);\n    memcpy(a, b, size);\n    memcpy(b, temp, size);\n}\n\nint main() {\n    int x = 10, y = 20;\n    genericSwap(&x, &y, sizeof(int));\n    cout << x << \" \" << y << endl;  // 20 10\n\n    double a = 1.5, b = 2.5;\n    genericSwap(&a, &b, sizeof(double));\n    cout << a << \" \" << b << endl;  // 2.5 1.5\n    return 0;\n}",
                        "explanation": "void* enables type-agnostic functions in C-style code. In C++, templates are preferred for this."
                    }
                ],
                "commonMistakes": [
                    "Dereferencing void* without casting — compilation error",
                    "Confusing int **pp with int (*pp)[N] (pointer to array)",
                    "Forgetting that C++ requires explicit cast from void* unlike C"
                ],
                "interviewTips": [
                    "Explain when you'd use void* vs templates (C compatibility, runtime type erasure)",
                    "Know why main(int argc, char **argv) uses double pointer",
                    "Be able to trace through double pointer dereferencing step by step"
                ]
            },
            {
                "id": "1.4",
                "title": "Const Pointers & Function Pointers",
                "explanation": "The const keyword with pointers has two independent dimensions:\n- `const int *p` (or `int const *p`): pointer to const — can't modify the value through p\n- `int *const p`: const pointer — can't change what p points to\n- `const int *const p`: both — can't modify value or change pointer\n\nFunction pointers store addresses of functions, enabling callbacks, strategy pattern, and jump tables. Read declarations right-to-left.",
                "keyPoints": [
                    "Read right-to-left: 'int *const p' = p is a const pointer to int",
                    "const int* and int const* are identical",
                    "Function pointer syntax: returnType (*name)(paramTypes)",
                    "typedef/using simplifies function pointer declarations",
                    "std::function is the modern C++ alternative to function pointers"
                ],
                "codeExamples": [
                    {
                        "title": "Const Correctness with Pointers",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    int x = 10, y = 20;\n\n    // Pointer to const: can't modify value through pointer\n    const int *p1 = &x;\n    // *p1 = 30;   // ERROR: can't modify\n    p1 = &y;       // OK: can change what it points to\n\n    // Const pointer: can't change the pointer itself\n    int *const p2 = &x;\n    *p2 = 30;      // OK: can modify the value\n    // p2 = &y;    // ERROR: can't repoint\n\n    // Const pointer to const: neither\n    const int *const p3 = &x;\n    // *p3 = 40;   // ERROR\n    // p3 = &y;    // ERROR\n\n    cout << x << endl; // 30 (modified through p2)\n    return 0;\n}",
                        "explanation": "The three levels of const with pointers. Read the declaration right-to-left to understand what's const."
                    },
                    {
                        "title": "Function Pointers and Callbacks",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <functional>\nusing namespace std;\n\nint add(int a, int b) { return a + b; }\nint multiply(int a, int b) { return a * b; }\n\n// Function pointer as parameter (callback)\nint compute(int x, int y, int (*op)(int, int)) {\n    return op(x, y);\n}\n\n// Using typedef for clarity\ntypedef int (*BinaryOp)(int, int);\n// Or modern: using BinaryOp = int(*)(int, int);\n\nint main() {\n    // Direct function pointer\n    int (*fp)(int, int) = &add;  // & is optional\n    cout << fp(3, 4) << endl;    // 7\n\n    // Callback pattern\n    cout << compute(5, 3, add) << endl;      // 8\n    cout << compute(5, 3, multiply) << endl; // 15\n\n    // Modern C++: std::function\n    function<int(int,int)> op = multiply;\n    cout << op(6, 7) << endl;  // 42\n\n    // Lambda as function pointer (if non-capturing)\n    auto sub = [](int a, int b) -> int { return a - b; };\n    cout << compute(10, 3, sub) << endl;  // 7\n    return 0;\n}",
                        "explanation": "Function pointers enable callbacks and strategy pattern. std::function is more flexible (accepts lambdas with captures)."
                    }
                ],
                "commonMistakes": [
                    "Confusing const int* with int* const",
                    "Forgetting that function name decays to function pointer automatically",
                    "Trying to use a capturing lambda where a function pointer is expected"
                ],
                "interviewTips": [
                    "Practice reading complex pointer declarations right-to-left",
                    "Know when to use function pointers vs std::function vs templates",
                    "Understand the const_cast use case: removing const for legacy C APIs"
                ]
            },
            {
                "id": "1.5",
                "title": "Dangling, Wild, and Null Pointers",
                "explanation": "Three dangerous pointer states:\n\n1. **Dangling pointer**: Points to memory that has been freed/deallocated or a local variable that went out of scope. Dereferencing is undefined behavior.\n\n2. **Wild pointer**: An uninitialized pointer containing a garbage address. Dereferencing is undefined behavior.\n\n3. **Null pointer**: Explicitly set to nullptr (C++) or NULL (C). Dereferencing crashes (segfault) but is at least deterministic. Always prefer nullptr over NULL in C++.\n\nnullptr has type std::nullptr_t and avoids ambiguity with integer 0 that NULL has.",
                "keyPoints": [
                    "Always initialize pointers (to nullptr if no valid address yet)",
                    "Set pointers to nullptr after delete to avoid dangling",
                    "Returning address of local variable creates a dangling pointer",
                    "Use-after-free is a critical security vulnerability (CWE-416)",
                    "nullptr is type-safe; NULL is just 0 and can cause overload ambiguity"
                ],
                "codeExamples": [
                    {
                        "title": "Dangling Pointer Scenarios",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\n// BAD: returns address of local variable\nint* dangling() {\n    int local = 42;\n    return &local;  // WARNING: dangling pointer!\n}\n\nint main() {\n    // Scenario 1: Use after free\n    int *p = new int(10);\n    delete p;\n    // *p = 20;  // UNDEFINED BEHAVIOR! p is dangling\n    p = nullptr; // Good practice: nullify after delete\n\n    // Scenario 2: Returning local address\n    int *bad = dangling();\n    // *bad is undefined behavior\n\n    // Scenario 3: Wild pointer\n    int *wild;    // uninitialized — contains garbage address\n    // *wild = 5; // UNDEFINED BEHAVIOR!\n\n    // Correct: always initialize\n    int *safe = nullptr;\n    if (safe != nullptr) {\n        cout << *safe << endl;\n    }\n    return 0;\n}",
                        "explanation": "Shows three common pointer bugs: use-after-free, returning local address, and wild pointers. Always initialize and nullify after delete."
                    }
                ],
                "commonMistakes": [
                    "Not setting pointer to nullptr after delete",
                    "Returning address of stack variable from a function",
                    "Using NULL instead of nullptr in C++ (ambiguity with int overloads)",
                    "Double-free: deleting the same pointer twice"
                ],
                "interviewTips": [
                    "Explain the difference between dangling, wild, and null pointers",
                    "Know that smart pointers (unique_ptr, shared_ptr) solve most of these problems",
                    "Understand why use-after-free is a security vulnerability"
                ]
            }
        ],
        "quizQuestions": [
            {
                "id": "q1.1",
                "type": "code_output",
                "difficulty": "easy",
                "question": "What is the output of this code?",
                "code": "int x = 5;\nint *p = &x;\n*p = *p + 10;\ncout << x;",
                "options": ["5", "10", "15", "Undefined"],
                "correctAnswer": "15",
                "explanation": "*p dereferences to x (value 5), adds 10, and stores 15 back through the pointer. x is now 15."
            },
            {
                "id": "q1.2",
                "type": "multiple_choice",
                "difficulty": "medium",
                "question": "What does `int *a, b;` declare?",
                "code": "",
                "options": ["Two pointers to int", "A pointer to int and an int", "Two ints", "Compilation error"],
                "correctAnswer": "A pointer to int and an int",
                "explanation": "The * binds to the variable name, not the type. Only 'a' is a pointer; 'b' is a regular int. To declare two pointers: int *a, *b;"
            },
            {
                "id": "q1.3",
                "type": "code_output",
                "difficulty": "medium",
                "question": "What is the output?",
                "code": "int arr[] = {10, 20, 30};\nint *p = arr;\ncout << *(p + 2) << \" \" << p[1];",
                "options": ["30 20", "20 30", "10 20", "Undefined"],
                "correctAnswer": "30 20",
                "explanation": "*(p+2) is arr[2]=30. p[1] is *(p+1)=arr[1]=20."
            },
            {
                "id": "q1.4",
                "type": "true_false",
                "difficulty": "easy",
                "question": "True or False: sizeof(int*) is always equal to sizeof(double*) on any given platform.",
                "code": "",
                "options": ["True", "False"],
                "correctAnswer": "True",
                "explanation": "All pointer types have the same size on a given platform since they all store memory addresses of the same width."
            },
            {
                "id": "q1.5",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "Which declaration means 'p is a constant pointer to a non-constant int'?",
                "code": "",
                "options": ["const int *p", "int const *p", "int *const p", "const int *const p"],
                "correctAnswer": "int *const p",
                "explanation": "Read right-to-left: 'p is const, pointer to int'. The pointer itself can't change, but the int it points to can be modified."
            },
            {
                "id": "q1.6",
                "type": "code_output",
                "difficulty": "hard",
                "question": "What is the output?",
                "code": "char s[] = \"Hello\";\nchar *p = s;\ncout << *(p+1) << p+1;",
                "options": ["eello", "eHello", "el", "Compilation error"],
                "correctAnswer": "eello",
                "explanation": "*(p+1) dereferences to 'e'. p+1 is a char* pointing to 'ello', which prints as the C-string 'ello'. Combined output: 'eello'."
            }
        ]
    }

def chapter_smart_pointers():
    return {
        "id": 2,
        "title": "Smart Pointers",
        "slug": "smart-pointers",
        "description": "Modern C++ memory management with unique_ptr, shared_ptr, and weak_ptr — RAII-based automatic resource management.",
        "icon": "🧠",
        "difficulty": "intermediate",
        "topics": [
            {
                "id": "2.1",
                "title": "std::unique_ptr — Exclusive Ownership",
                "explanation": "unique_ptr represents exclusive ownership of a dynamically allocated object. Only one unique_ptr can own a resource at a time. When the unique_ptr goes out of scope, it automatically deletes the managed object.\n\nKey: unique_ptr cannot be copied, only moved. This enforces single ownership at compile time.",
                "keyPoints": [
                    "Exclusive ownership — only one unique_ptr owns the resource",
                    "Cannot be copied (copy constructor/assignment deleted)",
                    "Can be moved with std::move() to transfer ownership",
                    "Use std::make_unique<T>(args) for exception-safe creation (C++14)",
                    "Zero overhead compared to raw pointer — no reference counting",
                    "Supports custom deleters and array types unique_ptr<T[]>"
                ],
                "codeExamples": [
                    {
                        "title": "unique_ptr Basics",
                        "language": "cpp",
                        "code": "#include <memory>\n#include <iostream>\nusing namespace std;\n\nclass Widget {\npublic:\n    Widget(int id) : id_(id) { cout << \"Widget \" << id_ << \" created\\n\"; }\n    ~Widget() { cout << \"Widget \" << id_ << \" destroyed\\n\"; }\n    void doWork() { cout << \"Widget \" << id_ << \" working\\n\"; }\nprivate:\n    int id_;\n};\n\nint main() {\n    // Prefer make_unique (C++14)\n    auto w1 = make_unique<Widget>(1);\n    w1->doWork();\n\n    // Transfer ownership\n    unique_ptr<Widget> w2 = move(w1);\n    // w1 is now nullptr\n    if (!w1) cout << \"w1 is null after move\\n\";\n    w2->doWork();\n\n    // unique_ptr for arrays\n    auto arr = make_unique<int[]>(5);\n    for (int i = 0; i < 5; i++) arr[i] = i * 10;\n\n    return 0;\n    // w2 auto-deleted here, arr auto-deleted here\n}",
                        "explanation": "unique_ptr automatically frees memory when it goes out of scope. Move semantics transfer ownership cleanly."
                    }
                ],
                "commonMistakes": [
                    "Trying to copy a unique_ptr (use std::move instead)",
                    "Using raw new instead of make_unique (exception safety issue)",
                    "Accessing a unique_ptr after moving it (it's nullptr)"
                ],
                "interviewTips": [
                    "Explain why unique_ptr has zero overhead vs raw pointers",
                    "Know when to use unique_ptr vs shared_ptr",
                    "unique_ptr is the default smart pointer — use it unless sharing is needed"
                ]
            },
            {
                "id": "2.2",
                "title": "std::shared_ptr — Shared Ownership",
                "explanation": "shared_ptr uses reference counting to allow multiple pointers to share ownership of an object. The object is deleted when the last shared_ptr owning it is destroyed.\n\nInternally maintains two counts: strong count (shared_ptrs) and weak count (weak_ptrs). The control block stores these counts and the deleter.",
                "keyPoints": [
                    "Multiple shared_ptrs can own the same object",
                    "Uses reference counting — object deleted when count reaches 0",
                    "Control block overhead: ~16-32 bytes per managed object",
                    "make_shared is more efficient (single allocation for object + control block)",
                    "Thread-safe reference counting (atomic increment/decrement)",
                    "NOT thread-safe for the pointed-to object itself"
                ],
                "codeExamples": [
                    {
                        "title": "shared_ptr Reference Counting",
                        "language": "cpp",
                        "code": "#include <memory>\n#include <iostream>\nusing namespace std;\n\nint main() {\n    auto sp1 = make_shared<int>(42);\n    cout << \"Count: \" << sp1.use_count() << endl; // 1\n\n    {\n        shared_ptr<int> sp2 = sp1;  // copy — count increases\n        cout << \"Count: \" << sp1.use_count() << endl; // 2\n\n        shared_ptr<int> sp3 = sp1;\n        cout << \"Count: \" << sp1.use_count() << endl; // 3\n    }\n    // sp2, sp3 destroyed — count decreases\n    cout << \"Count: \" << sp1.use_count() << endl; // 1\n\n    sp1.reset();  // releases ownership\n    cout << \"Count: \" << sp1.use_count() << endl; // 0\n    // Object is deleted here\n    return 0;\n}",
                        "explanation": "Reference count tracks how many shared_ptrs own the object. Object is deleted when count reaches zero."
                    }
                ],
                "commonMistakes": [
                    "Creating two shared_ptrs from the same raw pointer (double delete!)",
                    "Circular references causing memory leaks (use weak_ptr to break cycles)",
                    "Using shared_ptr when unique_ptr suffices (unnecessary overhead)"
                ],
                "interviewTips": [
                    "Explain the control block and why make_shared is preferred over shared_ptr(new T)",
                    "Know the cost: atomic ref count operations, control block allocation",
                    "Be ready to discuss thread safety nuances (ref count is atomic, object access is not)"
                ]
            },
            {
                "id": "2.3",
                "title": "std::weak_ptr — Breaking Circular References",
                "explanation": "weak_ptr is a non-owning observer of a shared_ptr-managed object. It doesn't affect the reference count and can detect if the object has been deleted (expired).\n\nPrimary use case: breaking circular references in data structures like doubly-linked lists, observer patterns, and caches.",
                "keyPoints": [
                    "Does not increment the strong reference count",
                    "Must be converted to shared_ptr via lock() before use",
                    "expired() checks if the managed object still exists",
                    "Essential for breaking circular references between shared_ptrs",
                    "Used in observer pattern, caches, and parent-child relationships"
                ],
                "codeExamples": [
                    {
                        "title": "Breaking Circular Reference with weak_ptr",
                        "language": "cpp",
                        "code": "#include <memory>\n#include <iostream>\nusing namespace std;\n\nstruct Node {\n    string name;\n    shared_ptr<Node> next;   // strong ownership forward\n    weak_ptr<Node> prev;     // weak reference back (breaks cycle!)\n\n    Node(string n) : name(n) { cout << name << \" created\\n\"; }\n    ~Node() { cout << name << \" destroyed\\n\"; }\n};\n\nint main() {\n    auto a = make_shared<Node>(\"A\");\n    auto b = make_shared<Node>(\"B\");\n\n    a->next = b;    // A owns B (strong)\n    b->prev = a;    // B observes A (weak — no cycle!)\n\n    // Check if weak_ptr is still valid\n    if (auto locked = b->prev.lock()) {\n        cout << \"B's prev is: \" << locked->name << endl;\n    }\n\n    return 0;\n    // Both A and B are properly destroyed\n}",
                        "explanation": "If prev were a shared_ptr, A and B would form a cycle and never be deleted. weak_ptr breaks the cycle."
                    }
                ],
                "commonMistakes": [
                    "Dereferencing weak_ptr directly (must call lock() first)",
                    "Not checking if lock() returns a valid shared_ptr",
                    "Using raw pointers instead of weak_ptr for back-references"
                ],
                "interviewTips": [
                    "Classic question: How do you solve circular reference with shared_ptr?",
                    "Know the observer pattern implementation with weak_ptr",
                    "Understand the difference between expired() and lock()"
                ]
            },
            {
                "id": "2.4",
                "title": "Custom Deleters & make_unique/make_shared",
                "explanation": "Smart pointers can use custom deleters for resources that aren't freed with delete (e.g., FILE*, C library handles, OS handles). make_unique and make_shared are factory functions that are exception-safe and (for shared_ptr) more efficient.",
                "keyPoints": [
                    "Custom deleter: unique_ptr<FILE, decltype(&fclose)> file(fopen(...), fclose)",
                    "make_shared combines object and control block in one allocation",
                    "make_unique prevents memory leaks in expressions with multiple news",
                    "shared_ptr deleter is type-erased (not part of the type)",
                    "unique_ptr deleter is part of the type (changes sizeof)"
                ],
                "codeExamples": [
                    {
                        "title": "Custom Deleter for C Resources",
                        "language": "cpp",
                        "code": "#include <memory>\n#include <cstdio>\n#include <iostream>\nusing namespace std;\n\nint main() {\n    // Custom deleter for FILE*\n    auto fileDeleter = [](FILE* f) {\n        if (f) {\n            fclose(f);\n            cout << \"File closed!\\n\";\n        }\n    };\n\n    {\n        unique_ptr<FILE, decltype(fileDeleter)> file(\n            fopen(\"test.txt\", \"w\"), fileDeleter\n        );\n        if (file) {\n            fprintf(file.get(), \"Hello Smart Pointers!\");\n        }\n    } // file automatically closed here\n\n    // shared_ptr with custom deleter (simpler syntax)\n    shared_ptr<FILE> file2(fopen(\"test2.txt\", \"w\"),\n        [](FILE* f) { if(f) fclose(f); }\n    );\n\n    return 0;\n}",
                        "explanation": "Custom deleters let smart pointers manage any resource, not just new/delete memory. FILE*, sockets, GPU handles, etc."
                    }
                ],
                "commonMistakes": [
                    "Forgetting that unique_ptr's deleter changes its type",
                    "Not using make_shared/make_unique when possible",
                    "Creating shared_ptr from raw pointer in multiple places"
                ],
                "interviewTips": [
                    "Explain why make_shared is more efficient (single allocation)",
                    "Know the exception safety argument for make_unique",
                    "Discuss RAII and how smart pointers generalize it"
                ]
            }
        ],
        "quizQuestions": [
            {
                "id": "q2.1",
                "type": "multiple_choice",
                "difficulty": "easy",
                "question": "Which smart pointer allows multiple owners of the same object?",
                "code": "",
                "options": ["unique_ptr", "shared_ptr", "weak_ptr", "auto_ptr"],
                "correctAnswer": "shared_ptr",
                "explanation": "shared_ptr uses reference counting to allow shared ownership. unique_ptr has exclusive ownership. weak_ptr is non-owning."
            },
            {
                "id": "q2.2",
                "type": "code_output",
                "difficulty": "medium",
                "question": "What is the output?",
                "code": "auto sp = make_shared<int>(10);\nauto sp2 = sp;\nauto sp3 = move(sp);\ncout << sp.use_count() << \" \" << sp2.use_count();",
                "options": ["0 2", "1 2", "0 3", "1 3"],
                "correctAnswer": "0 2",
                "explanation": "After move, sp is null (count 0). sp2 and sp3 share ownership, so sp2.use_count() is 2."
            },
            {
                "id": "q2.3",
                "type": "true_false",
                "difficulty": "medium",
                "question": "True or False: unique_ptr has zero runtime overhead compared to a raw pointer.",
                "code": "",
                "options": ["True", "False"],
                "correctAnswer": "True",
                "explanation": "unique_ptr with default deleter compiles to the same machine code as raw pointer + delete. No reference counting, no control block."
            },
            {
                "id": "q2.4",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "What problem does weak_ptr solve?",
                "code": "",
                "options": ["Thread safety", "Circular references causing memory leaks", "Array allocation", "Exception handling"],
                "correctAnswer": "Circular references causing memory leaks",
                "explanation": "When two objects hold shared_ptrs to each other, their reference counts never reach 0. weak_ptr breaks the cycle."
            },
            {
                "id": "q2.5",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "Why is make_shared<T>() preferred over shared_ptr<T>(new T())?",
                "code": "",
                "options": ["It's faster because it combines object and control block into one allocation", "It prevents memory leaks in complex expressions", "Both A and B", "Neither, they are equivalent"],
                "correctAnswer": "Both A and B",
                "explanation": "make_shared does a single allocation (efficiency) and avoids the leak scenario where new succeeds but shared_ptr construction fails."
            }
        ]
    }

def chapter_memory():
    return {
        "id": 3,
        "title": "Memory Management",
        "slug": "memory-management",
        "description": "Stack vs heap, memory layout, RAII pattern, new/delete vs malloc/free, memory alignment, and leak detection.",
        "icon": "💾",
        "difficulty": "advanced",
        "topics": [
            {
                "id": "3.1",
                "title": "Stack vs Heap Memory",
                "explanation": "Stack: Fast, automatic (LIFO), limited size (~1-8MB), stores local variables and function call frames. Allocation/deallocation is just pointer movement.\n\nHeap: Slower, manual/dynamic, virtually unlimited, stores dynamically allocated objects. Uses system calls (brk/mmap). Subject to fragmentation.",
                "keyPoints": [
                    "Stack: O(1) alloc/dealloc, contiguous, cache-friendly, auto lifetime",
                    "Heap: O(n) alloc (first-fit/best-fit), fragmentation, manual lifetime",
                    "Stack overflow: deep recursion or large local arrays",
                    "Heap fragmentation: many small alloc/free cycles leave holes",
                    "Modern allocators (jemalloc, tcmalloc) use arenas and thread-local caches"
                ],
                "codeExamples": [
                    {
                        "title": "Stack vs Heap Allocation",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nvoid stackExample() {\n    int arr[100];        // Stack: fast, fixed size, auto cleanup\n    arr[0] = 42;\n    // arr destroyed when function returns\n}\n\nvoid heapExample() {\n    int *arr = new int[100]; // Heap: slower, flexible size\n    arr[0] = 42;\n    delete[] arr;            // MUST manually free!\n}\n\nint main() {\n    int local = 10;          // Stack\n    int *dynamic = new int(20); // Heap\n\n    cout << \"Stack addr: \" << &local << endl;    // High address\n    cout << \"Heap addr:  \" << dynamic << endl;   // Low address\n\n    delete dynamic;\n    return 0;\n}",
                        "explanation": "Stack variables are automatic; heap variables require explicit management. Stack addresses are typically higher than heap on most systems."
                    }
                ],
                "commonMistakes": [
                    "Allocating large arrays on the stack (stack overflow)",
                    "Forgetting delete/delete[] for heap allocations",
                    "Mixing delete with new[] or delete[] with new"
                ],
                "interviewTips": [
                    "Draw the memory layout: text, data, BSS, heap (grows up), stack (grows down)",
                    "Explain why stack is faster (pointer bump vs free-list search)",
                    "Know typical stack sizes and how to change them"
                ]
            },
            {
                "id": "3.2",
                "title": "new/delete vs malloc/free",
                "explanation": "C++ new/delete: type-safe, calls constructors/destructors, throws std::bad_alloc on failure.\n\nC malloc/free: returns void*, no constructors, returns NULL on failure.\n\nNever mix them: don't free() memory from new, don't delete memory from malloc.",
                "keyPoints": [
                    "new calls constructor; malloc only allocates raw memory",
                    "delete calls destructor; free only releases memory",
                    "new throws std::bad_alloc; malloc returns NULL on failure",
                    "new[] pairs with delete[]; new pairs with delete",
                    "placement new constructs an object at a specific address",
                    "Use nothrow version: new(nothrow) int returns nullptr on failure"
                ],
                "codeExamples": [
                    {
                        "title": "new/delete vs malloc/free",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <cstdlib>\nusing namespace std;\n\nclass MyClass {\npublic:\n    MyClass() { cout << \"Constructor called\\n\"; }\n    ~MyClass() { cout << \"Destructor called\\n\"; }\n};\n\nint main() {\n    // C++ way: constructor IS called\n    MyClass *obj1 = new MyClass();  // Constructor called\n    delete obj1;                     // Destructor called\n\n    // C way: constructor NOT called\n    MyClass *obj2 = (MyClass*)malloc(sizeof(MyClass));\n    // obj2 is uninitialized raw memory!\n    free(obj2);  // Destructor NOT called\n\n    // Arrays\n    int *arr = new int[5]{1,2,3,4,5};\n    delete[] arr;  // MUST use delete[], not delete\n\n    // Placement new: construct at specific address\n    char buffer[sizeof(MyClass)];\n    MyClass *placed = new (buffer) MyClass();  // Construct in buffer\n    placed->~MyClass();  // Must manually call destructor!\n    // Do NOT delete placed — it's on the stack!\n\n    return 0;\n}",
                        "explanation": "new/delete integrate with C++ object model (constructors/destructors). malloc/free are raw memory operations."
                    }
                ],
                "commonMistakes": [
                    "Using delete instead of delete[] for arrays",
                    "Mixing malloc with delete or new with free",
                    "Forgetting to call destructor explicitly with placement new"
                ],
                "interviewTips": [
                    "Explain the full sequence: new = operator new (allocate) + constructor",
                    "Know that operator new can be overloaded globally or per-class",
                    "Understand placement new use cases (memory pools, embedded systems)"
                ]
            },
            {
                "id": "3.3",
                "title": "Process Memory Layout",
                "explanation": "A typical process memory layout (low to high address):\n1. Text segment: executable code (read-only)\n2. Data segment: initialized global/static variables\n3. BSS segment: uninitialized global/static variables (zero-initialized)\n4. Heap: grows upward, dynamic allocations\n5. Memory-mapped region: shared libraries, mmap\n6. Stack: grows downward, local variables and call frames",
                "keyPoints": [
                    "Text segment is read-only and shared between processes",
                    "BSS stands for Block Started by Symbol — zero-initialized",
                    "Heap grows toward higher addresses",
                    "Stack grows toward lower addresses",
                    "Stack and heap can collide if both grow too much",
                    "Each thread has its own stack but shares the heap"
                ],
                "codeExamples": [
                    {
                        "title": "Memory Segments Visualization",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nint global_init = 42;      // Data segment\nint global_uninit;         // BSS segment\nstatic int static_var = 7; // Data segment\nconst char *str = \"hello\"; // str in Data, \"hello\" in Text/rodata\n\nint main() {\n    int local = 10;            // Stack\n    static int s_local = 5;    // Data segment (not stack!)\n    int *heap = new int(20);   // Heap\n\n    cout << \"Code (func addr):  \" << (void*)&main << endl;\n    cout << \"Global init:       \" << &global_init << endl;\n    cout << \"Global uninit:     \" << &global_uninit << endl;\n    cout << \"Static:            \" << &static_var << endl;\n    cout << \"Heap:              \" << heap << endl;\n    cout << \"Stack (local):     \" << &local << endl;\n\n    delete heap;\n    return 0;\n}",
                        "explanation": "Observe the address ranges: code < data/BSS < heap < ... < stack. Static locals go in data segment, not stack."
                    }
                ],
                "commonMistakes": [
                    "Thinking static local variables are on the stack",
                    "Not understanding that string literals are in read-only memory",
                    "Ignoring that each thread has its own stack"
                ],
                "interviewTips": [
                    "Be able to draw the memory layout diagram from memory",
                    "Know where each type of variable lives (global, static, local, dynamic)",
                    "Understand virtual memory and page tables at a high level"
                ]
            },
            {
                "id": "3.4",
                "title": "RAII — Resource Acquisition Is Initialization",
                "explanation": "RAII is the most important C++ idiom. Resources (memory, files, locks, sockets) are acquired in the constructor and released in the destructor. This guarantees cleanup even when exceptions occur.\n\nEvery smart pointer, std::lock_guard, std::fstream, and std::vector follows RAII.",
                "keyPoints": [
                    "Acquire resources in constructor, release in destructor",
                    "Guarantees cleanup even if exceptions are thrown",
                    "Eliminates manual cleanup code and error-prone goto patterns",
                    "Smart pointers are RAII wrappers for heap memory",
                    "lock_guard/unique_lock are RAII wrappers for mutexes",
                    "RAII is sometimes called SBRM (Scope-Bound Resource Management)"
                ],
                "codeExamples": [
                    {
                        "title": "RAII for File Handling",
                        "language": "cpp",
                        "code": "#include <fstream>\n#include <iostream>\n#include <stdexcept>\nusing namespace std;\n\nclass FileWriter {\n    FILE* file_;\npublic:\n    FileWriter(const char* path) : file_(fopen(path, \"w\")) {\n        if (!file_) throw runtime_error(\"Cannot open file\");\n    }\n    ~FileWriter() {\n        if (file_) fclose(file_);  // Always cleaned up!\n    }\n    void write(const char* text) {\n        fprintf(file_, \"%s\", text);\n    }\n    // Delete copy to prevent double-close\n    FileWriter(const FileWriter&) = delete;\n    FileWriter& operator=(const FileWriter&) = delete;\n};\n\nvoid process() {\n    FileWriter fw(\"output.txt\");  // Resource acquired\n    fw.write(\"Hello RAII!\");\n    // Even if an exception is thrown here,\n    // ~FileWriter() still runs and closes the file\n}  // fw destroyed, file closed automatically",
                        "explanation": "RAII ensures the file is always closed, even if an exception occurs between opening and the function returning."
                    }
                ],
                "commonMistakes": [
                    "Not following RAII, using manual cleanup with error-prone if/goto",
                    "Forgetting to delete copy operations for non-copyable resources",
                    "Calling destructors explicitly (almost never needed)"
                ],
                "interviewTips": [
                    "RAII is THE answer to 'How does C++ manage resources without GC?'",
                    "Connect RAII to smart pointers, lock_guard, and the Rule of 5",
                    "Explain how RAII interacts with exception handling"
                ]
            },
            {
                "id": "3.5",
                "title": "Memory Alignment & Padding",
                "explanation": "CPUs access memory most efficiently at aligned addresses (address divisible by data size). Compilers add padding bytes to structs to maintain alignment. This affects struct size and is crucial for hardware interaction, network protocols, and cache performance.",
                "keyPoints": [
                    "Alignment requirement: address must be divisible by sizeof(type)",
                    "Compiler inserts padding between struct members for alignment",
                    "Struct size is rounded up to a multiple of the largest member's alignment",
                    "Reorder members largest-to-smallest to minimize padding",
                    "#pragma pack or __attribute__((packed)) disables padding (use carefully)",
                    "alignas(N) specifies custom alignment (C++11)"
                ],
                "codeExamples": [
                    {
                        "title": "Struct Padding and Reordering",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\n// Bad ordering: 24 bytes with padding\nstruct BadLayout {\n    char a;      // 1 byte + 7 padding\n    double b;    // 8 bytes\n    char c;      // 1 byte + 3 padding\n    int d;       // 4 bytes\n};               // Total: 24 bytes\n\n// Good ordering: 16 bytes, minimal padding\nstruct GoodLayout {\n    double b;    // 8 bytes\n    int d;       // 4 bytes\n    char a;      // 1 byte\n    char c;      // 1 byte + 2 padding\n};               // Total: 16 bytes\n\nint main() {\n    cout << \"BadLayout:  \" << sizeof(BadLayout) << endl;  // 24\n    cout << \"GoodLayout: \" << sizeof(GoodLayout) << endl; // 16\n    return 0;\n}",
                        "explanation": "Reordering struct members from largest to smallest alignment saves 33% memory here. Critical for cache performance in arrays."
                    }
                ],
                "commonMistakes": [
                    "Assuming struct size equals sum of member sizes",
                    "Using packed structs for performance (it actually hurts due to unaligned access)",
                    "Not considering alignment in network/file serialization"
                ],
                "interviewTips": [
                    "Be able to calculate struct sizes with padding on the spot",
                    "Know alignof() and alignas() operators",
                    "Explain why cache line alignment (64 bytes) matters for performance"
                ]
            }
        ],
        "quizQuestions": [
            {
                "id": "q3.1",
                "type": "multiple_choice",
                "difficulty": "easy",
                "question": "Where are local variables stored?",
                "code": "",
                "options": ["Heap", "Stack", "Data segment", "BSS segment"],
                "correctAnswer": "Stack",
                "explanation": "Local (automatic) variables are stored on the stack and automatically destroyed when the function returns."
            },
            {
                "id": "q3.2",
                "type": "code_output",
                "difficulty": "medium",
                "question": "What is the output?",
                "code": "struct S { char a; int b; char c; };\ncout << sizeof(S);",
                "options": ["6", "8", "12", "9"],
                "correctAnswer": "12",
                "explanation": "char a (1) + 3 padding + int b (4) + char c (1) + 3 padding = 12. Struct size rounds up to multiple of largest alignment (4)."
            },
            {
                "id": "q3.3",
                "type": "multiple_choice",
                "difficulty": "medium",
                "question": "What does RAII stand for and what does it guarantee?",
                "code": "",
                "options": [
                    "Resource Acquisition Is Initialization — resources freed in destructor",
                    "Runtime Allocation Is Immediate — fast memory allocation",
                    "Reference And Indirection Interface — pointer abstraction",
                    "Resource Allocation In Implementation — implementation detail"
                ],
                "correctAnswer": "Resource Acquisition Is Initialization — resources freed in destructor",
                "explanation": "RAII ties resource lifetime to object lifetime. Constructor acquires, destructor releases — even if exceptions occur."
            },
            {
                "id": "q3.4",
                "type": "true_false",
                "difficulty": "easy",
                "question": "True or False: malloc calls the constructor of a C++ class.",
                "code": "",
                "options": ["True", "False"],
                "correctAnswer": "False",
                "explanation": "malloc only allocates raw memory. Only new calls constructors. Similarly, free doesn't call destructors."
            },
            {
                "id": "q3.5",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "What happens if you use delete instead of delete[] for an array allocated with new[]?",
                "code": "int *arr = new int[10];\ndelete arr; // instead of delete[] arr;",
                "options": ["Compiles and works fine", "Compilation error", "Undefined behavior", "Only the first element is deleted"],
                "correctAnswer": "Undefined behavior",
                "explanation": "Mismatching new[] with delete is undefined behavior. For class types, it may only call one destructor instead of N."
            }
        ]
    }

def chapter_bit_manipulation():
    return {
        "id": 4,
        "title": "Bit Manipulation",
        "slug": "bit-manipulation",
        "description": "Bitwise operators, bit tricks, bit fields, and essential bit manipulation idioms used in systems and embedded programming.",
        "icon": "⚡",
        "difficulty": "intermediate",
        "topics": [
            {
                "id": "4.1",
                "title": "Bitwise Operators",
                "explanation": "C/C++ provides six bitwise operators:\n- AND (&): Both bits must be 1\n- OR (|): Either bit can be 1\n- XOR (^): Bits must differ\n- NOT (~): Flips all bits\n- Left Shift (<<): Multiply by 2^n\n- Right Shift (>>): Divide by 2^n (arithmetic for signed, logical for unsigned)",
                "keyPoints": [
                    "AND (&) is used for masking (extracting specific bits)",
                    "OR (|) is used for setting bits",
                    "XOR (^) is used for toggling bits and has unique properties (a^a=0, a^0=a)",
                    "Left shift by n multiplies by 2^n",
                    "Right shift of signed integers is implementation-defined (usually arithmetic)",
                    "Shifting by >= bit width is undefined behavior"
                ],
                "codeExamples": [
                    {
                        "title": "Bitwise Operator Basics",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <bitset>\nusing namespace std;\n\nint main() {\n    unsigned int a = 0b1100;  // 12\n    unsigned int b = 0b1010;  // 10\n\n    cout << \"a & b  = \" << bitset<4>(a & b) << endl;   // 1000 (8)\n    cout << \"a | b  = \" << bitset<4>(a | b) << endl;   // 1110 (14)\n    cout << \"a ^ b  = \" << bitset<4>(a ^ b) << endl;   // 0110 (6)\n    cout << \"~a     = \" << bitset<32>(~a) << endl;     // all flipped\n    cout << \"a << 1 = \" << (a << 1) << endl;           // 24\n    cout << \"a >> 1 = \" << (a >> 1) << endl;           // 6\n    return 0;\n}",
                        "explanation": "Demonstrates all six bitwise operators with binary visualization using std::bitset."
                    }
                ],
                "commonMistakes": [
                    "Confusing && (logical AND) with & (bitwise AND)",
                    "Shifting a 32-bit int by 32 or more (undefined behavior)",
                    "Right-shifting negative numbers (implementation-defined)"
                ],
                "interviewTips": [
                    "Know XOR properties cold: a^a=0, a^0=a, a^b^a=b",
                    "Understand operator precedence: & has lower precedence than ==",
                    "Use parentheses: if ((x & mask) == expected) — not x & mask == expected"
                ]
            },
            {
                "id": "4.2",
                "title": "Essential Bit Tricks",
                "explanation": "Common bit manipulation idioms that appear frequently in interviews and systems programming.",
                "keyPoints": [
                    "Set bit i:    n |= (1 << i)",
                    "Clear bit i:  n &= ~(1 << i)",
                    "Toggle bit i: n ^= (1 << i)",
                    "Check bit i:  (n >> i) & 1",
                    "Power of 2 check: n > 0 && (n & (n-1)) == 0",
                    "Lowest set bit: n & (-n)",
                    "Clear lowest set bit: n & (n-1)",
                    "Swap without temp: a ^= b; b ^= a; a ^= b;"
                ],
                "codeExamples": [
                    {
                        "title": "Bit Manipulation Toolkit",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <bitset>\nusing namespace std;\n\nint main() {\n    int n = 0b1010;  // 10\n\n    // Set bit 0 -> 1011 (11)\n    cout << bitset<4>(n | (1 << 0)) << endl;\n\n    // Clear bit 1 -> 1000 (8)\n    cout << bitset<4>(n & ~(1 << 1)) << endl;\n\n    // Toggle bit 3 -> 0010 (2)\n    cout << bitset<4>(n ^ (1 << 3)) << endl;\n\n    // Check if bit 1 is set\n    cout << \"Bit 1: \" << ((n >> 1) & 1) << endl; // 1\n\n    // Power of 2?\n    int p = 16;\n    cout << p << \" is power of 2: \" << (p > 0 && (p & (p-1)) == 0) << endl;\n\n    // Count set bits (Brian Kernighan's algorithm)\n    int count = 0;\n    int x = 0b1011011;\n    while (x) {\n        x &= (x - 1);  // clears lowest set bit\n        count++;\n    }\n    cout << \"Set bits: \" << count << endl;  // 5\n\n    // Swap without temp\n    int a = 5, b = 3;\n    a ^= b; b ^= a; a ^= b;\n    cout << \"a=\" << a << \" b=\" << b << endl; // a=3 b=5\n    return 0;\n}",
                        "explanation": "Essential bit tricks: set/clear/toggle/check bits, power-of-2 check, Kernighan's bit counting, XOR swap."
                    }
                ],
                "commonMistakes": [
                    "Forgetting parentheses: (1 << i) needs parens due to operator precedence",
                    "XOR swap fails when a and b are the same variable (zeroes it out)",
                    "Using signed int for bit manipulation (sign bit complications)"
                ],
                "interviewTips": [
                    "Memorize: n & (n-1) clears lowest set bit — used in many problems",
                    "Know Brian Kernighan's algorithm for counting set bits",
                    "Understand two's complement for negative number representation"
                ]
            },
            {
                "id": "4.3",
                "title": "Bit Fields & Bitmasks",
                "explanation": "Bit fields allow packing multiple values into a single integer using specific bit ranges. Used extensively in network protocols, hardware registers, and flags.\n\nBitmasks define which bits to extract or modify. Common in permission systems (Unix file permissions), hardware programming, and feature flags.",
                "keyPoints": [
                    "Bit fields: struct { unsigned int flag : 1; unsigned int mode : 3; };",
                    "Bitmask pattern: flags |= MASK to set, flags &= ~MASK to clear",
                    "Use enum or constexpr for named bitmask constants",
                    "Bit fields are non-portable (ordering and padding are implementation-defined)",
                    "Prefer explicit bit manipulation over bit fields for portability"
                ],
                "codeExamples": [
                    {
                        "title": "Bitmask Flags Pattern",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\n// Permission flags (like Unix file permissions)\nconstexpr unsigned int READ    = 1 << 0;  // 0001\nconstexpr unsigned int WRITE   = 1 << 1;  // 0010\nconstexpr unsigned int EXECUTE = 1 << 2;  // 0100\nconstexpr unsigned int ADMIN   = 1 << 3;  // 1000\n\nvoid printPerms(unsigned int perms) {\n    if (perms & READ)    cout << \"READ \";\n    if (perms & WRITE)   cout << \"WRITE \";\n    if (perms & EXECUTE) cout << \"EXECUTE \";\n    if (perms & ADMIN)   cout << \"ADMIN \";\n    cout << endl;\n}\n\nint main() {\n    unsigned int perms = 0;\n\n    perms |= READ | WRITE;     // Grant read and write\n    printPerms(perms);          // READ WRITE\n\n    perms |= EXECUTE;          // Add execute\n    printPerms(perms);          // READ WRITE EXECUTE\n\n    perms &= ~WRITE;           // Revoke write\n    printPerms(perms);          // READ EXECUTE\n\n    perms ^= ADMIN;            // Toggle admin\n    printPerms(perms);          // READ EXECUTE ADMIN\n    return 0;\n}",
                        "explanation": "Bitmask flags are used everywhere: file permissions, network protocol headers, GPU feature flags, CPU status registers."
                    }
                ],
                "commonMistakes": [
                    "Relying on bit field ordering across compilers (it's implementation-defined)",
                    "Using signed types for bitmask operations",
                    "Not using constexpr/enum class for flag constants"
                ],
                "interviewTips": [
                    "Know real-world uses: TCP flags, UNIX permissions, hardware registers",
                    "Explain why enum class with overloaded operators is preferred for type-safe flags",
                    "Relevant for Qualcomm/Ericsson: protocol header parsing uses bitmasks extensively"
                ]
            },
            {
                "id": "4.4",
                "title": "Endianness & Byte Ordering",
                "explanation": "Endianness defines how multi-byte values are stored in memory:\n- Big-endian: Most significant byte at lowest address (network byte order)\n- Little-endian: Least significant byte at lowest address (x86, ARM default)\n\nCritical for network programming, file formats, and cross-platform serialization. Telecom protocols (5G, LTE) use big-endian (network byte order).",
                "keyPoints": [
                    "x86 and ARM (default) are little-endian",
                    "Network protocols use big-endian (network byte order)",
                    "Use htons/htonl to convert host to network byte order",
                    "Use ntohs/ntohl to convert network to host byte order",
                    "Endianness only matters for multi-byte types, not single bytes"
                ],
                "codeExamples": [
                    {
                        "title": "Detecting and Handling Endianness",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <cstdint>\nusing namespace std;\n\nbool isLittleEndian() {\n    uint32_t num = 1;\n    // If least significant byte is at lowest address\n    return *reinterpret_cast<uint8_t*>(&num) == 1;\n}\n\n// Manual byte swap (big-endian <-> little-endian)\nuint32_t byteSwap32(uint32_t x) {\n    return ((x >> 24) & 0xFF)       |\n           ((x >> 8)  & 0xFF00)     |\n           ((x << 8)  & 0xFF0000)   |\n           ((x << 24) & 0xFF000000);\n}\n\nint main() {\n    cout << \"System is \" << (isLittleEndian() ? \"little\" : \"big\")\n         << \"-endian\" << endl;\n\n    uint32_t val = 0x12345678;\n    uint32_t swapped = byteSwap32(val);\n    cout << hex << \"Original: 0x\" << val << endl;\n    cout << hex << \"Swapped:  0x\" << swapped << endl;\n    // Original: 0x12345678\n    // Swapped:  0x78563412\n    return 0;\n}",
                        "explanation": "Endianness detection and byte swapping — essential for network/telecom programming."
                    }
                ],
                "commonMistakes": [
                    "Sending multi-byte data over network without byte order conversion",
                    "Assuming all systems have the same endianness",
                    "Using memcpy between hosts with different endianness without conversion"
                ],
                "interviewTips": [
                    "Ericsson/Qualcomm/Nokia will ask about network byte order in telecom context",
                    "Know htons, htonl, ntohs, ntohl and when to use each",
                    "Be able to write byteSwap by hand"
                ]
            }
        ],
        "quizQuestions": [
            {
                "id": "q4.1",
                "type": "code_output",
                "difficulty": "easy",
                "question": "What is the value of x?",
                "code": "int x = 12 & 10;  // 1100 & 1010",
                "options": ["8", "14", "6", "2"],
                "correctAnswer": "8",
                "explanation": "1100 & 1010 = 1000 = 8. AND keeps only bits that are 1 in both operands."
            },
            {
                "id": "q4.2",
                "type": "code_output",
                "difficulty": "medium",
                "question": "What does this expression evaluate to?",
                "code": "int n = 16;\nbool result = (n > 0) && ((n & (n - 1)) == 0);",
                "options": ["true", "false", "16", "Undefined"],
                "correctAnswer": "true",
                "explanation": "n=16=10000. n-1=15=01111. n & (n-1) = 0. So 16 is a power of 2."
            },
            {
                "id": "q4.3",
                "type": "multiple_choice",
                "difficulty": "medium",
                "question": "How do you clear bit i in integer n?",
                "code": "",
                "options": ["n &= (1 << i)", "n |= ~(1 << i)", "n &= ~(1 << i)", "n ^= (1 << i)"],
                "correctAnswer": "n &= ~(1 << i)",
                "explanation": "~(1 << i) creates a mask with all bits set except bit i. ANDing with n clears only bit i."
            },
            {
                "id": "q4.4",
                "type": "code_output",
                "difficulty": "hard",
                "question": "How many times does this loop execute for n = 255?",
                "code": "int count = 0;\nwhile (n) {\n    n &= (n - 1);\n    count++;\n}",
                "options": ["7", "8", "255", "1"],
                "correctAnswer": "8",
                "explanation": "This is Kernighan's algorithm. 255 = 11111111 has 8 set bits. Each iteration clears one set bit, so the loop runs 8 times."
            },
            {
                "id": "q4.5",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "In network programming (e.g., 5G protocol stack), what byte order is used?",
                "code": "",
                "options": ["Little-endian", "Big-endian (network byte order)", "Implementation-defined", "UTF-8 encoding order"],
                "correctAnswer": "Big-endian (network byte order)",
                "explanation": "Network protocols use big-endian by convention (RFC 1700). Use htons/htonl to convert from host to network byte order."
            }
        ]
    }

def chapter_classes_oop():
    return {
        "id": 5,
        "title": "Classes & OOP",
        "slug": "classes-oop",
        "description": "Constructors, destructors, Rule of 3/5/0, virtual functions & vtable, inheritance, polymorphism, and the diamond problem.",
        "icon": "🏗️",
        "difficulty": "intermediate",
        "topics": [
            {
                "id": "5.1",
                "title": "Constructors, Destructors & Rule of 3/5/0",
                "explanation": "Special member functions control object lifecycle:\n- Default constructor: no args\n- Parameterized constructor: custom init\n- Copy constructor: T(const T&)\n- Move constructor: T(T&&)\n- Copy assignment: T& operator=(const T&)\n- Move assignment: T& operator=(T&&)\n- Destructor: ~T()\n\nRule of 3 (C++98): If you define destructor, copy constructor, or copy assignment — define all three.\nRule of 5 (C++11): Add move constructor and move assignment.\nRule of 0: Prefer using smart pointers/containers so you need NONE of these.",
                "keyPoints": [
                    "Compiler generates defaults unless you declare any special member function",
                    "If you declare a destructor, compiler won't generate move operations",
                    "= default forces compiler generation; = delete prevents usage",
                    "Use member initializer lists for efficiency (avoids default-then-assign)",
                    "Delegating constructors (C++11) can call other constructors"
                ],
                "codeExamples": [
                    {
                        "title": "Rule of 5 Implementation",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <cstring>\n#include <utility>\nusing namespace std;\n\nclass String {\n    char* data_;\n    size_t size_;\npublic:\n    // Constructor\n    String(const char* s = \"\") : size_(strlen(s)) {\n        data_ = new char[size_ + 1];\n        strcpy(data_, s);\n        cout << \"Constructed: \" << data_ << \"\\n\";\n    }\n\n    // Destructor\n    ~String() {\n        delete[] data_;\n    }\n\n    // Copy constructor (deep copy)\n    String(const String& other) : size_(other.size_) {\n        data_ = new char[size_ + 1];\n        strcpy(data_, other.data_);\n        cout << \"Copy constructed: \" << data_ << \"\\n\";\n    }\n\n    // Move constructor (steal resources)\n    String(String&& other) noexcept : data_(other.data_), size_(other.size_) {\n        other.data_ = nullptr;\n        other.size_ = 0;\n        cout << \"Move constructed\\n\";\n    }\n\n    // Copy assignment (copy-and-swap idiom)\n    String& operator=(String other) {  // pass by value = copy\n        swap(data_, other.data_);\n        swap(size_, other.size_);\n        return *this;\n    }\n    // Move assignment handled by copy assignment via pass-by-value\n};",
                        "explanation": "Complete Rule of 5 with copy-and-swap idiom. Move constructor steals resources instead of copying — O(1) vs O(n)."
                    }
                ],
                "commonMistakes": [
                    "Shallow copy when class owns resources (double-free!)",
                    "Not marking move constructor noexcept (prevents use with std::vector)",
                    "Forgetting to nullify moved-from object's pointers"
                ],
                "interviewTips": [
                    "Know copy-and-swap idiom and why it provides strong exception safety",
                    "Explain why Rule of 0 is preferred in modern C++",
                    "Know that std::move doesn't move — it casts to rvalue reference"
                ]
            },
            {
                "id": "5.2",
                "title": "Virtual Functions & vtable",
                "explanation": "Virtual functions enable runtime polymorphism. When a function is declared virtual, calls through base pointers/references are dispatched to the correct derived class version at runtime.\n\nImplementation: compiler creates a vtable (array of function pointers) for each class with virtual functions. Each object gets a hidden vptr pointing to its class's vtable.",
                "keyPoints": [
                    "virtual keyword enables dynamic dispatch",
                    "override keyword (C++11) catches errors if base function doesn't exist",
                    "vtable: per-class table of function pointers",
                    "vptr: per-object hidden pointer to the vtable (adds sizeof(void*) to object)",
                    "Virtual destructor is essential if deleting through base pointer",
                    "Pure virtual (= 0) makes a class abstract",
                    "Virtual function call has slight overhead: indirect function call through vptr"
                ],
                "codeExamples": [
                    {
                        "title": "Virtual Functions and vtable Mechanism",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nclass Shape {\npublic:\n    virtual double area() const = 0;   // Pure virtual\n    virtual void draw() const {         // Virtual with default\n        cout << \"Drawing shape\\n\";\n    }\n    virtual ~Shape() = default;         // Virtual destructor!\n};\n\nclass Circle : public Shape {\n    double radius_;\npublic:\n    Circle(double r) : radius_(r) {}\n    double area() const override { return 3.14159 * radius_ * radius_; }\n    void draw() const override { cout << \"Drawing circle r=\" << radius_ << \"\\n\"; }\n};\n\nclass Rectangle : public Shape {\n    double w_, h_;\npublic:\n    Rectangle(double w, double h) : w_(w), h_(h) {}\n    double area() const override { return w_ * h_; }\n    void draw() const override { cout << \"Drawing rect \" << w_ << \"x\" << h_ << \"\\n\"; }\n};\n\nint main() {\n    // Polymorphism through base pointer\n    Shape* shapes[] = { new Circle(5), new Rectangle(3, 4) };\n    for (auto s : shapes) {\n        s->draw();   // Dynamic dispatch via vtable\n        cout << \"Area: \" << s->area() << \"\\n\";\n        delete s;    // Correct destructor called (virtual!)\n    }\n    return 0;\n}",
                        "explanation": "Virtual functions enable polymorphism. Without virtual, the base class version would always be called through a base pointer."
                    }
                ],
                "commonMistakes": [
                    "Forgetting virtual destructor in base class (undefined behavior when deleting through base pointer)",
                    "Calling virtual functions in constructor/destructor (no polymorphism!)",
                    "Not using override keyword, silently creating a new function instead of overriding"
                ],
                "interviewTips": [
                    "Draw the vtable layout for a class hierarchy",
                    "Explain the cost of virtual functions (indirect call, cache miss potential)",
                    "Know that virtual functions in constructors resolve to the current class, not derived"
                ]
            },
            {
                "id": "5.3",
                "title": "Inheritance & Diamond Problem",
                "explanation": "C++ supports multiple inheritance, which can lead to the diamond problem: if B and C both inherit from A, and D inherits from both B and C, D gets two copies of A's members.\n\nSolution: virtual inheritance ensures only one copy of the base class exists.",
                "keyPoints": [
                    "public inheritance: IS-A relationship",
                    "protected inheritance: changes public members to protected in derived",
                    "private inheritance: IS-IMPLEMENTED-IN-TERMS-OF relationship",
                    "Diamond problem: D inherits A through both B and C",
                    "Virtual inheritance: class B : virtual public A — single copy of A",
                    "Virtual base classes add overhead (virtual base table pointer)"
                ],
                "codeExamples": [
                    {
                        "title": "Diamond Problem & Virtual Inheritance",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nclass Animal {\npublic:\n    int age = 0;\n    void breathe() { cout << \"Breathing\\n\"; }\n};\n\n// Virtual inheritance prevents duplicate Animal\nclass Mammal : virtual public Animal {\npublic:\n    void walk() { cout << \"Walking\\n\"; }\n};\n\nclass Bird : virtual public Animal {\npublic:\n    void fly() { cout << \"Flying\\n\"; }\n};\n\n// Without virtual: Bat would have TWO copies of Animal\n// With virtual: only ONE copy of Animal\nclass Bat : public Mammal, public Bird {\npublic:\n    void sonar() { cout << \"Using sonar\\n\"; }\n};\n\nint main() {\n    Bat bat;\n    bat.age = 5;    // Unambiguous with virtual inheritance\n    bat.breathe();  // Unambiguous — only one Animal\n    bat.walk();\n    bat.fly();\n    bat.sonar();\n    return 0;\n}",
                        "explanation": "Virtual inheritance ensures one copy of Animal in Bat. Without virtual, bat.age would be ambiguous."
                    }
                ],
                "commonMistakes": [
                    "Forgetting virtual keyword leads to ambiguous member access",
                    "Not understanding that virtual base class constructors are called by the most derived class",
                    "Overusing multiple inheritance — prefer composition"
                ],
                "interviewTips": [
                    "Be able to explain the diamond problem with a diagram",
                    "Know that virtual inheritance adds a vbptr (virtual base table pointer)",
                    "Discuss composition over inheritance as a design principle"
                ]
            },
            {
                "id": "5.4",
                "title": "Copy & Move Semantics",
                "explanation": "Copy semantics create independent copies of objects. Move semantics (C++11) transfer resources from one object to another without copying, converting expensive deep copies into cheap pointer swaps.\n\nKey: std::move doesn't actually move anything — it's just a cast to rvalue reference (T&&), which enables the move constructor/assignment to be called.",
                "keyPoints": [
                    "Lvalue: named object, has address. Rvalue: temporary, about to be destroyed",
                    "std::move() casts to rvalue reference — enables move semantics",
                    "Move constructor/assignment should leave source in valid but unspecified state",
                    "Mark move operations noexcept for optimal container performance",
                    "RVO (Return Value Optimization) often eliminates copies/moves entirely",
                    "std::forward preserves value category for perfect forwarding"
                ],
                "codeExamples": [
                    {
                        "title": "Move Semantics Performance",
                        "language": "cpp",
                        "code": "#include <iostream>\n#include <vector>\n#include <string>\nusing namespace std;\n\nint main() {\n    string s1 = \"Hello World - this is a long string\";\n    cout << \"s1: \" << s1 << endl;\n\n    // Copy: allocates new memory, copies chars\n    string s2 = s1;\n    cout << \"After copy, s1: \" << s1 << endl;  // s1 unchanged\n\n    // Move: steals s1's internal buffer\n    string s3 = move(s1);\n    cout << \"After move, s1: '\" << s1 << \"'\" << endl;  // s1 is empty!\n    cout << \"s3: \" << s3 << endl;  // has the data\n\n    // Move with containers\n    vector<string> v;\n    string data = \"important data\";\n    v.push_back(move(data));  // Moved into vector, O(1)\n    // data is now empty\n\n    return 0;\n}",
                        "explanation": "Move semantics turn O(n) copies into O(1) resource transfers. The source object is left in a valid but empty state."
                    }
                ],
                "commonMistakes": [
                    "Using an object after std::move (it's in unspecified state)",
                    "Thinking std::move actually moves something (it's just a cast)",
                    "Not marking move operations noexcept (vector will copy instead of move!)"
                ],
                "interviewTips": [
                    "Explain lvalue vs rvalue and how && (rvalue reference) works",
                    "Know that RVO/NRVO can eliminate copies entirely — even better than move",
                    "Explain perfect forwarding with std::forward and why it matters for templates"
                ]
            },
            {
                "id": "5.5",
                "title": "Operator Overloading & static Members",
                "explanation": "C++ allows most operators to be overloaded for user-defined types, enabling natural syntax. Some operators must be member functions (=, [], (), ->), others are better as free functions (+, -, ==, <<).\n\nStatic members belong to the class, not instances. Static member functions can only access static members.",
                "keyPoints": [
                    "Overload operators to make types behave like built-in types",
                    "operator= must be a member function",
                    "operator<< (stream output) should be a friend or free function",
                    "Static data members: shared across all instances, defined outside class",
                    "Static member functions: no 'this' pointer, can't access non-static members",
                    "Spaceship operator <=> (C++20) generates all comparison operators"
                ],
                "codeExamples": [
                    {
                        "title": "Operator Overloading Example",
                        "language": "cpp",
                        "code": "#include <iostream>\nusing namespace std;\n\nclass Vector2D {\n    double x_, y_;\npublic:\n    Vector2D(double x = 0, double y = 0) : x_(x), y_(y) {}\n\n    // Member operator\n    Vector2D operator+(const Vector2D& rhs) const {\n        return {x_ + rhs.x_, y_ + rhs.y_};\n    }\n\n    bool operator==(const Vector2D& rhs) const {\n        return x_ == rhs.x_ && y_ == rhs.y_;\n    }\n\n    // Friend for stream output\n    friend ostream& operator<<(ostream& os, const Vector2D& v) {\n        return os << \"(\" << v.x_ << \", \" << v.y_ << \")\";\n    }\n\n    // Static member\n    static int instanceCount;\n};\n\nint Vector2D::instanceCount = 0; // Define static member\n\nint main() {\n    Vector2D a(1, 2), b(3, 4);\n    Vector2D c = a + b;  // operator+\n    cout << c << endl;   // operator<< : (4, 6)\n    cout << (a == b) << endl;  // 0 (false)\n    return 0;\n}",
                        "explanation": "Operator overloading enables natural syntax. Static members are shared across all instances."
                    }
                ],
                "commonMistakes": [
                    "Overloading operator&& or operator|| (breaks short-circuit evaluation)",
                    "Forgetting to return *this from assignment operator",
                    "Not defining static members outside the class"
                ],
                "interviewTips": [
                    "Know which operators can/cannot be overloaded",
                    "Explain why operator<< is usually a friend function (left operand is ostream)",
                    "Know the C++20 spaceship operator <=> for automatic comparison generation"
                ]
            }
        ],
        "quizQuestions": [
            {
                "id": "q5.1",
                "type": "multiple_choice",
                "difficulty": "medium",
                "question": "What is the Rule of 5 in C++11?",
                "code": "",
                "options": [
                    "If you define any of: destructor, copy constructor, copy assignment, move constructor, move assignment — define all five",
                    "A class should have at most 5 member variables",
                    "Inheritance hierarchy should be at most 5 levels deep",
                    "Functions should have at most 5 parameters"
                ],
                "correctAnswer": "If you define any of: destructor, copy constructor, copy assignment, move constructor, move assignment — define all five",
                "explanation": "The Rule of 5 extends the Rule of 3 to include move semantics. If you manage resources, you likely need all five."
            },
            {
                "id": "q5.2",
                "type": "true_false",
                "difficulty": "medium",
                "question": "True or False: Virtual functions can exhibit polymorphic behavior when called inside a constructor.",
                "code": "",
                "options": ["True", "False"],
                "correctAnswer": "False",
                "explanation": "In a constructor, the vtable points to the current class, not the derived class. Virtual calls resolve to the constructor's own class version."
            },
            {
                "id": "q5.3",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "What happens if a base class has a non-virtual destructor and you delete a derived object through a base pointer?",
                "code": "Base *p = new Derived();\ndelete p;",
                "options": ["Only base destructor runs", "Only derived destructor runs", "Both destructors run correctly", "Undefined behavior"],
                "correctAnswer": "Undefined behavior",
                "explanation": "Deleting a derived object through a base pointer without a virtual destructor is undefined behavior per the standard."
            },
            {
                "id": "q5.4",
                "type": "code_output",
                "difficulty": "medium",
                "question": "What is the output?",
                "code": "class A { public: virtual void f() { cout << \"A\"; } };\nclass B : public A { public: void f() override { cout << \"B\"; } };\nA *p = new B();\np->f();\ndelete p;",
                "options": ["A", "B", "AB", "Compilation error"],
                "correctAnswer": "B",
                "explanation": "f() is virtual. p points to a B object, so B::f() is called through dynamic dispatch via the vtable."
            },
            {
                "id": "q5.5",
                "type": "multiple_choice",
                "difficulty": "hard",
                "question": "What does std::move(x) actually do?",
                "code": "",
                "options": ["Moves the data from x to a new location", "Casts x to an rvalue reference", "Deletes x", "Copies x and then deletes the original"],
                "correctAnswer": "Casts x to an rvalue reference",
                "explanation": "std::move is just a cast to T&&. It enables the move constructor/assignment to be selected, but doesn't move anything itself."
            }
        ]
    }

def chapter_templates():
    return {
        "id": 6, "title": "Templates & Generic Programming", "slug": "templates-generic",
        "description": "Function/class templates, specialization, SFINAE, variadic templates, CRTP, and C++20 concepts.",
        "icon": "🔧", "difficulty": "advanced",
        "topics": [
            {"id": "6.1", "title": "Function & Class Templates",
             "explanation": "Templates enable writing generic code that works with any type. The compiler generates specific versions (instantiations) for each type used. Function templates deduce types from arguments; class templates require explicit specification (before C++17 CTAD).",
             "keyPoints": ["template<typename T> syntax", "Implicit type deduction for functions", "Class Template Argument Deduction (CTAD) in C++17", "Templates are compiled at instantiation, not definition", "Code bloat risk: each instantiation generates new code"],
             "codeExamples": [{"title": "Generic Max Function", "language": "cpp",
                "code": "#include <iostream>\nusing namespace std;\n\ntemplate<typename T>\nT myMax(T a, T b) {\n    return (a > b) ? a : b;\n}\n\ntemplate<typename T>\nclass Stack {\n    T data[100];\n    int top = -1;\npublic:\n    void push(T val) { data[++top] = val; }\n    T pop() { return data[top--]; }\n    bool empty() const { return top == -1; }\n};\n\nint main() {\n    cout << myMax(3, 7) << endl;        // int version\n    cout << myMax(3.14, 2.72) << endl;  // double version\n    cout << myMax<string>(\"abc\", \"xyz\") << endl; // explicit\n\n    Stack<int> s;\n    s.push(10); s.push(20);\n    cout << s.pop() << endl;  // 20\n    return 0;\n}",
                "explanation": "Templates generate type-specific code at compile time. Zero runtime overhead."}],
             "commonMistakes": ["Defining templates in .cpp files (linker error — must be in headers)", "Not understanding that each instantiation is separate code"],
             "interviewTips": ["Explain how templates differ from Java/C# generics (compile-time vs runtime)", "Know about template argument deduction rules"]},
            {"id": "6.2", "title": "Template Specialization",
             "explanation": "Full specialization provides a completely different implementation for a specific type. Partial specialization (class templates only) specializes based on patterns.",
             "keyPoints": ["Full specialization: template<> class Foo<int> {...}", "Partial specialization works on class templates, not function templates", "Use overloading instead of function template specialization", "Specialization must be declared after the primary template"],
             "codeExamples": [{"title": "Template Specialization", "language": "cpp",
                "code": "#include <iostream>\n#include <cstring>\nusing namespace std;\n\n// Primary template\ntemplate<typename T>\nbool isEqual(T a, T b) { return a == b; }\n\n// Full specialization for C-strings\ntemplate<>\nbool isEqual<const char*>(const char* a, const char* b) {\n    return strcmp(a, b) == 0;\n}\n\n// Partial specialization (class template)\ntemplate<typename T>\nclass Storage { T data; public: void set(T d) { data = d; } };\n\ntemplate<typename T>\nclass Storage<T*> {  // Specialization for pointer types\n    T* data;\npublic:\n    void set(T* d) { data = d; }\n    T deref() { return *data; }\n};\n\nint main() {\n    cout << isEqual(1, 1) << endl;                   // 1 (true)\n    cout << isEqual(\"hello\", \"hello\") << endl;       // 1 (specialized)\n    return 0;\n}",
                "explanation": "Specialization customizes template behavior for specific types. Essential for optimizing string comparisons, pointer handling, etc."}],
             "commonMistakes": ["Trying to partially specialize function templates", "Forgetting template<> for full specialization"],
             "interviewTips": ["Know the difference between specialization and overloading", "Explain when to use specialization vs if constexpr (C++17)"]},
            {"id": "6.3", "title": "Variadic Templates & Fold Expressions",
             "explanation": "Variadic templates accept any number of template arguments using parameter packs (typename... Args). Combined with fold expressions (C++17), they enable powerful compile-time operations on argument lists.",
             "keyPoints": ["Parameter pack: typename... Args, Args... args", "sizeof...(Args) gives the number of arguments", "Fold expressions (C++17): (args + ...) folds over all args", "Used in std::tuple, std::make_unique, std::variant", "Recursive unpacking pattern for pre-C++17 code"],
             "codeExamples": [{"title": "Variadic Template Print", "language": "cpp",
                "code": "#include <iostream>\nusing namespace std;\n\n// C++17 fold expression version\ntemplate<typename... Args>\nvoid print(Args... args) {\n    ((cout << args << \" \"), ...);\n    cout << endl;\n}\n\n// Sum using fold expression\ntemplate<typename... Args>\nauto sum(Args... args) {\n    return (args + ...);\n}\n\nint main() {\n    print(1, 2.5, \"hello\", 'A');  // 1 2.5 hello A\n    cout << sum(1, 2, 3, 4, 5) << endl;  // 15\n    return 0;\n}",
                "explanation": "Variadic templates with fold expressions provide concise, type-safe variadic functions — the modern replacement for C's va_args."}],
             "commonMistakes": ["Forgetting the base case in recursive unpacking (pre-C++17)", "Not understanding pack expansion rules"],
             "interviewTips": ["Know how std::make_unique uses perfect forwarding with variadic templates", "Explain the difference between variadic templates and C varargs (type safety)"]},
            {"id": "6.4", "title": "CRTP & Concepts (C++20)",
             "explanation": "CRTP (Curiously Recurring Template Pattern): A class inherits from a template instantiated with itself. Enables static polymorphism (no vtable overhead).\n\nConcepts (C++20): Named constraints on template parameters. Replace SFINAE with readable syntax.",
             "keyPoints": ["CRTP: class Derived : public Base<Derived>", "Static polymorphism: dispatch resolved at compile time, no virtual overhead", "Concepts: template<Sortable T> replaces template<typename T> + SFINAE", "requires clause for ad-hoc constraints", "Concepts produce better error messages than SFINAE"],
             "codeExamples": [{"title": "CRTP and Concepts", "language": "cpp",
                "code": "#include <iostream>\n#include <concepts>\nusing namespace std;\n\n// CRTP: Static polymorphism\ntemplate<typename Derived>\nclass Shape {\npublic:\n    void draw() {\n        static_cast<Derived*>(this)->drawImpl();\n    }\n};\n\nclass Circle : public Shape<Circle> {\npublic:\n    void drawImpl() { cout << \"Drawing circle\\n\"; }\n};\n\n// C++20 Concept\ntemplate<typename T>\nconcept Numeric = requires(T a, T b) {\n    { a + b } -> convertible_to<T>;\n    { a * b } -> convertible_to<T>;\n};\n\ntemplate<Numeric T>\nT multiply(T a, T b) { return a * b; }\n\nint main() {\n    Circle c;\n    c.draw();  // Static dispatch, no vtable!\n    cout << multiply(3, 4) << endl;     // 12\n    cout << multiply(2.5, 3.0) << endl; // 7.5\n    // multiply(\"a\", \"b\"); // Compile error with clear message!\n    return 0;\n}",
                "explanation": "CRTP provides polymorphism without virtual function overhead. Concepts constrain templates with readable, meaningful error messages."}],
             "commonMistakes": ["Infinite recursion in CRTP if drawImpl is missing", "Overcomplicating SFINAE when concepts would suffice"],
             "interviewTips": ["Know CRTP use cases: static polymorphism, mixin classes", "Nvidia/Google increasingly ask about C++20 concepts"]}
        ],
        "quizQuestions": [
            {"id": "q6.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "Where should template definitions be placed?", "code": "",
             "options": ["In .cpp files", "In header files", "In a separate .tpp file linked at runtime", "Anywhere"],
             "correctAnswer": "In header files",
             "explanation": "Templates must be visible at the point of instantiation. Placing them in .cpp files causes linker errors because the compiler can't instantiate them from other translation units."},
            {"id": "q6.2", "type": "multiple_choice", "difficulty": "medium",
             "question": "What is CRTP used for?", "code": "",
             "options": ["Runtime polymorphism", "Static (compile-time) polymorphism", "Memory management", "Thread synchronization"],
             "correctAnswer": "Static (compile-time) polymorphism",
             "explanation": "CRTP achieves polymorphism at compile time through template instantiation, avoiding the overhead of virtual function dispatch."},
            {"id": "q6.3", "type": "code_output", "difficulty": "medium",
             "question": "What does sizeof...(args) return for: template<typename... Args> void f(Args... args) called as f(1, 2.0, \"hi\")?", "code": "",
             "options": ["3", "12", "0", "Compilation error"],
             "correctAnswer": "3",
             "explanation": "sizeof...(args) returns the number of arguments in the parameter pack, which is 3."},
            {"id": "q6.4", "type": "multiple_choice", "difficulty": "hard",
             "question": "What problem do C++20 concepts solve?", "code": "",
             "options": ["Memory leaks", "Unreadable SFINAE error messages and constraints", "Thread safety", "Dynamic dispatch overhead"],
             "correctAnswer": "Unreadable SFINAE error messages and constraints",
             "explanation": "Concepts provide named, readable constraints for template parameters, replacing cryptic SFINAE techniques and producing clear error messages."},
            {"id": "q6.5", "type": "true_false", "difficulty": "medium",
             "question": "True or False: Function templates can be partially specialized.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "False",
             "explanation": "Only class templates support partial specialization. For function templates, use overloading instead."}
        ]
    }

def chapter_stl_containers():
    return {
        "id": 7, "title": "STL Containers & Iterators", "slug": "stl-containers",
        "description": "Vector, map, unordered_map, set, deque, iterator categories, and iterator invalidation rules.",
        "icon": "📦", "difficulty": "intermediate",
        "topics": [
            {"id": "7.1", "title": "Sequence Containers: vector, deque, list",
             "explanation": "vector: Dynamic array, contiguous memory, O(1) random access, amortized O(1) push_back. The most used container.\ndeque: Double-ended queue, O(1) push_front and push_back, not fully contiguous.\nlist: Doubly linked list, O(1) insert/erase anywhere with iterator, O(n) access.",
             "keyPoints": ["vector: contiguous memory = cache-friendly, capacity doubles on growth", "deque: fixed-size blocks, O(1) front/back operations", "list: no random access, but O(1) splice and iterator stability", "Prefer vector by default — it's fastest for most use cases", "reserve() prevents reallocations if you know the size upfront"],
             "codeExamples": [{"title": "Container Comparison", "language": "cpp",
                "code": "#include <iostream>\n#include <vector>\n#include <deque>\n#include <list>\nusing namespace std;\n\nint main() {\n    // Vector: best general-purpose container\n    vector<int> v = {1, 2, 3};\n    v.push_back(4);        // Amortized O(1)\n    v[2] = 30;             // O(1) random access\n    // v.push_front(0);    // NOT available — O(n)\n\n    // Deque: fast at both ends\n    deque<int> d = {1, 2, 3};\n    d.push_front(0);       // O(1)\n    d.push_back(4);        // O(1)\n    d[2] = 30;             // O(1) random access\n\n    // List: fast insert/erase with iterator\n    list<int> l = {1, 2, 3};\n    auto it = l.begin(); advance(it, 1);\n    l.insert(it, 15);     // O(1) insert at position\n    // l[2];              // NOT available — no random access\n\n    return 0;\n}",
                "explanation": "Choose vector for most cases, deque for double-ended operations, list only when you need stable iterators and constant-time splicing."}],
             "commonMistakes": ["Using list when vector would be faster (cache locality matters more than O(1) insert)", "Not calling reserve() on vector when size is known"],
             "interviewTips": ["Know the time complexity of every operation for each container", "Explain why vector is usually faster than list even for middle insertions (cache effects)"]},
            {"id": "7.2", "title": "Associative Containers: map, set, unordered_map",
             "explanation": "map/set: Red-black tree based, O(log n) operations, keys are sorted.\nunordered_map/unordered_set: Hash table based, O(1) average operations, no ordering.\nmultimap/multiset: Allow duplicate keys.",
             "keyPoints": ["map: sorted keys, O(log n) lookup/insert/erase", "unordered_map: hash table, O(1) average, O(n) worst case", "map preserves insertion order by key; unordered_map does not", "Custom comparators for map, custom hash for unordered_map", "emplace() constructs in-place, avoiding unnecessary copies"],
             "codeExamples": [{"title": "map vs unordered_map", "language": "cpp",
                "code": "#include <iostream>\n#include <map>\n#include <unordered_map>\nusing namespace std;\n\nint main() {\n    // Sorted map (red-black tree)\n    map<string, int> m;\n    m[\"banana\"] = 2;\n    m[\"apple\"] = 5;\n    m[\"cherry\"] = 3;\n    for (auto& [k, v] : m)\n        cout << k << \": \" << v << endl;\n    // apple: 5, banana: 2, cherry: 3 (sorted!)\n\n    // Hash map (average O(1))\n    unordered_map<string, int> um;\n    um[\"banana\"] = 2;\n    um[\"apple\"] = 5;\n    um.insert({\"cherry\", 3});\n    // Iteration order is NOT guaranteed\n\n    // Check existence\n    if (um.count(\"apple\")) cout << \"Found apple\\n\";\n    if (um.find(\"grape\") == um.end()) cout << \"No grape\\n\";\n\n    return 0;\n}",
                "explanation": "Use map when you need sorted keys; unordered_map for fastest average lookup. Both are critical for interviews."}],
             "commonMistakes": ["Using [] on a const map (it inserts default if key missing!)", "Not providing hash function for custom types in unordered_map"],
             "interviewTips": ["Know when to use map vs unordered_map (sorted needs vs speed)", "Be ready to implement a simple hash table from scratch"]},
            {"id": "7.3", "title": "Iterator Categories & Invalidation",
             "explanation": "Iterator categories (weakest to strongest): Input, Output, Forward, Bidirectional, Random Access, Contiguous (C++20).\n\nIterator invalidation: operations like push_back, erase, insert can invalidate existing iterators. Rules differ per container.",
             "keyPoints": ["vector: any reallocation invalidates ALL iterators; insert/erase invalidates from that point onward", "deque: insert/erase at ends keeps iterators valid (mostly)", "list/set/map: only iterators to erased elements are invalidated", "unordered_map: rehashing invalidates all iterators", "Use returned iterator from erase() for safe removal while iterating"],
             "codeExamples": [{"title": "Safe Erase While Iterating", "language": "cpp",
                "code": "#include <iostream>\n#include <vector>\n#include <list>\nusing namespace std;\n\nint main() {\n    // WRONG way to erase from vector\n    // for (auto it = v.begin(); it != v.end(); ++it)\n    //     if (*it % 2 == 0) v.erase(it); // UNDEFINED!\n\n    // RIGHT way: use returned iterator\n    vector<int> v = {1, 2, 3, 4, 5, 6};\n    for (auto it = v.begin(); it != v.end(); ) {\n        if (*it % 2 == 0)\n            it = v.erase(it);  // erase returns next valid iterator\n        else\n            ++it;\n    }\n    // v = {1, 3, 5}\n\n    // Even better: erase-remove idiom\n    vector<int> v2 = {1, 2, 3, 4, 5, 6};\n    v2.erase(remove_if(v2.begin(), v2.end(),\n        [](int x) { return x % 2 == 0; }), v2.end());\n    // v2 = {1, 3, 5}\n\n    // C++20: std::erase_if\n    // erase_if(v2, [](int x) { return x % 2 == 0; });\n    return 0;\n}",
                "explanation": "Iterator invalidation is a major source of bugs. Always use the return value of erase() or the erase-remove idiom."}],
             "commonMistakes": ["Erasing from a vector while iterating with range-based for", "Assuming iterators are valid after push_back (they're not if reallocation occurs)"],
             "interviewTips": ["Memorize iterator invalidation rules for vector, map, unordered_map", "Know the erase-remove idiom — it's a classic interview question"]}
        ],
        "quizQuestions": [
            {"id": "q7.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "Which STL container provides O(1) random access and contiguous memory?", "code": "",
             "options": ["list", "deque", "vector", "set"],
             "correctAnswer": "vector",
             "explanation": "vector uses contiguous memory like an array, providing O(1) random access via operator[]."},
            {"id": "q7.2", "type": "multiple_choice", "difficulty": "medium",
             "question": "What happens when you use map::operator[] with a key that doesn't exist?", "code": "",
             "options": ["Returns end iterator", "Throws an exception", "Inserts a default-constructed value", "Returns 0"],
             "correctAnswer": "Inserts a default-constructed value",
             "explanation": "operator[] inserts a default-constructed value if the key doesn't exist. Use find() or at() to avoid unintended insertion."},
            {"id": "q7.3", "type": "multiple_choice", "difficulty": "hard",
             "question": "After calling push_back on a vector, which iterators are guaranteed to remain valid?", "code": "",
             "options": ["All iterators", "No iterators (if reallocation occurs)", "Only end() iterator", "All except end()"],
             "correctAnswer": "No iterators (if reallocation occurs)",
             "explanation": "If push_back triggers reallocation, ALL iterators, pointers, and references are invalidated. If no reallocation, only end() is invalidated."},
            {"id": "q7.4", "type": "multiple_choice", "difficulty": "medium",
             "question": "What is the time complexity of std::map::find()?", "code": "",
             "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
             "correctAnswer": "O(log n)",
             "explanation": "std::map is implemented as a red-black tree (balanced BST), so find() is O(log n). Use unordered_map for O(1) average."}
        ]
    }

def chapter_stl_algorithms():
    return {
        "id": 8, "title": "STL Algorithms & Lambdas", "slug": "stl-algorithms",
        "description": "Key STL algorithms, lambda expressions, std::function, and functional programming patterns.",
        "icon": "⚙️", "difficulty": "intermediate",
        "topics": [
            {"id": "8.1", "title": "Essential Algorithms: sort, find, transform, accumulate",
             "explanation": "STL provides 100+ algorithms in <algorithm> and <numeric>. They operate on iterators, making them container-agnostic.",
             "keyPoints": ["sort: O(n log n) introsort, works on random-access iterators", "find/find_if: linear search, returns iterator to first match", "transform: applies function to each element, stores result", "accumulate: reduces range to single value (fold)", "All algorithms work on any container via iterators"],
             "codeExamples": [{"title": "Common STL Algorithms", "language": "cpp",
                "code": "#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <numeric>\nusing namespace std;\n\nint main() {\n    vector<int> v = {5, 2, 8, 1, 9, 3};\n\n    // Sort\n    sort(v.begin(), v.end()); // {1,2,3,5,8,9}\n    sort(v.begin(), v.end(), greater<int>()); // {9,8,5,3,2,1}\n\n    // Find\n    auto it = find(v.begin(), v.end(), 5);\n    if (it != v.end()) cout << \"Found 5 at index \" << (it - v.begin()) << endl;\n\n    // Find_if with lambda\n    auto even = find_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });\n\n    // Transform: square each element\n    vector<int> squared(v.size());\n    transform(v.begin(), v.end(), squared.begin(), [](int x) { return x * x; });\n\n    // Accumulate: sum\n    int sum = accumulate(v.begin(), v.end(), 0);\n    cout << \"Sum: \" << sum << endl;\n\n    // Count_if\n    int evens = count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });\n    cout << \"Even count: \" << evens << endl;\n\n    return 0;\n}",
                "explanation": "STL algorithms + lambdas = expressive, efficient code. Know these cold for interviews."}],
             "commonMistakes": ["Sorting a list with std::sort (list has its own sort method)", "Forgetting initial value in accumulate (can cause type mismatch)"],
             "interviewTips": ["Know the complexity of major algorithms", "Prefer STL algorithms over hand-written loops"]},
            {"id": "8.2", "title": "Lambda Expressions",
             "explanation": "Lambdas (C++11) are anonymous function objects. Syntax: [capture](params) -> return_type { body }\n\nCapture modes: [=] by value, [&] by reference, [x, &y] specific captures, [this] captures this pointer.",
             "keyPoints": ["[=] captures all by value, [&] all by reference", "[x] captures x by value, [&x] by reference", "Mutable lambdas: [x]() mutable { x++; } allows modifying captured values", "Generic lambdas (C++14): [](auto x) { ... }", "Lambdas without captures can convert to function pointers"],
             "codeExamples": [{"title": "Lambda Capture Modes", "language": "cpp",
                "code": "#include <iostream>\n#include <vector>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    int threshold = 5;\n    vector<int> v = {1, 7, 3, 9, 2, 8};\n\n    // Capture by value\n    auto above = [threshold](int x) { return x > threshold; };\n    cout << count_if(v.begin(), v.end(), above) << \" above 5\" << endl;\n\n    // Capture by reference (modifies outer variable)\n    int sum = 0;\n    for_each(v.begin(), v.end(), [&sum](int x) { sum += x; });\n    cout << \"Sum: \" << sum << endl;\n\n    // Generic lambda (C++14)\n    auto print = [](const auto& x) { cout << x << \" \"; };\n    for_each(v.begin(), v.end(), print);\n    cout << endl;\n\n    // Mutable lambda\n    int counter = 0;\n    auto count = [counter]() mutable { return ++counter; };\n    cout << count() << count() << count() << endl; // 123\n\n    // Immediately invoked lambda (IIFE)\n    const auto config = []() {\n        // complex initialization logic\n        return 42;\n    }();\n\n    return 0;\n}",
                "explanation": "Lambdas are essential modern C++. Capture modes control which outer variables are accessible and how."}],
             "commonMistakes": ["Capturing by reference when the lambda outlives the variable (dangling reference)", "Forgetting mutable when modifying captured-by-value variables"],
             "interviewTips": ["Know all capture modes and when to use each", "Explain how lambdas are implemented (compiler generates a functor class)"]}
        ],
        "quizQuestions": [
            {"id": "q8.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "What does [&] in a lambda capture clause mean?", "code": "",
             "options": ["Capture nothing", "Capture all by value", "Capture all by reference", "Capture this pointer"],
             "correctAnswer": "Capture all by reference",
             "explanation": "[&] captures all local variables used in the lambda body by reference."},
            {"id": "q8.2", "type": "code_output", "difficulty": "medium",
             "question": "What is the output?", "code": "vector<int> v = {3, 1, 4, 1, 5};\nsort(v.begin(), v.end(), greater<int>());\ncout << v[0] << v[4];",
             "options": ["13", "51", "31", "53"],
             "correctAnswer": "51",
             "explanation": "greater<int>() sorts in descending order: {5,4,3,1,1}. v[0]=5, v[4]=1."},
            {"id": "q8.3", "type": "true_false", "difficulty": "medium",
             "question": "True or False: A lambda with no captures can be implicitly converted to a function pointer.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "True",
             "explanation": "Non-capturing lambdas are convertible to function pointers of matching signature, since they don't need a closure."},
            {"id": "q8.4", "type": "multiple_choice", "difficulty": "hard",
             "question": "What is the time complexity of std::sort?", "code": "",
             "options": ["O(n)", "O(n log n) guaranteed", "O(n log n) average, O(n^2) worst", "O(n log n) worst case (introsort)"],
             "correctAnswer": "O(n log n) worst case (introsort)",
             "explanation": "std::sort uses introsort: quicksort + heapsort fallback + insertion sort for small ranges. Guaranteed O(n log n)."}
        ]
    }

def chapter_concurrency():
    return {
        "id": 9, "title": "Concurrency & Multithreading", "slug": "concurrency",
        "description": "Threads, mutexes, atomics, condition variables, async/futures, and common concurrency patterns.",
        "icon": "🔀", "difficulty": "advanced",
        "topics": [
            {"id": "9.1", "title": "std::thread, mutex, lock_guard",
             "explanation": "std::thread launches a new thread of execution. Shared data must be protected with mutexes. lock_guard/unique_lock provide RAII-based locking.",
             "keyPoints": ["std::thread t(func, args...) launches a thread", "Must call t.join() or t.detach() before thread object is destroyed", "std::mutex protects shared data (lock/unlock)", "std::lock_guard: RAII lock — locks in constructor, unlocks in destructor", "std::unique_lock: flexible RAII lock — supports deferred locking, condition variables", "std::scoped_lock (C++17): locks multiple mutexes without deadlock"],
             "codeExamples": [{"title": "Thread-Safe Counter", "language": "cpp",
                "code": "#include <iostream>\n#include <thread>\n#include <mutex>\n#include <vector>\nusing namespace std;\n\nclass Counter {\n    int count_ = 0;\n    mutex mtx_;\npublic:\n    void increment() {\n        lock_guard<mutex> lock(mtx_);  // RAII lock\n        ++count_;\n    }\n    int get() const { return count_; }\n};\n\nint main() {\n    Counter counter;\n    vector<thread> threads;\n\n    for (int i = 0; i < 10; i++) {\n        threads.emplace_back([&counter]() {\n            for (int j = 0; j < 1000; j++)\n                counter.increment();\n        });\n    }\n\n    for (auto& t : threads) t.join();\n    cout << \"Count: \" << counter.get() << endl; // 10000\n    return 0;\n}",
                "explanation": "lock_guard ensures the mutex is always unlocked, even if an exception occurs. Without it, forgetting to unlock causes deadlock."}],
             "commonMistakes": ["Forgetting to join or detach threads (program terminates!)", "Locking multiple mutexes in different order (deadlock)", "Data races: accessing shared data without protection"],
             "interviewTips": ["Know the difference between lock_guard, unique_lock, and scoped_lock", "Explain deadlock conditions (mutual exclusion, hold-and-wait, no preemption, circular wait)", "Qualcomm/Ericsson heavily test concurrency for telecom systems"]},
            {"id": "9.2", "title": "Atomic Operations & Condition Variables",
             "explanation": "std::atomic provides lock-free thread-safe operations on individual variables. std::condition_variable enables threads to wait for events (producer-consumer pattern).",
             "keyPoints": ["atomic<int>: lock-free increment, compare-exchange, load, store", "Faster than mutex for simple operations on single variables", "condition_variable: wait/notify pattern for thread coordination", "Always use condition_variable with a predicate to handle spurious wakeups", "memory_order controls instruction reordering (seq_cst is default and safest)"],
             "codeExamples": [{"title": "Producer-Consumer Pattern", "language": "cpp",
                "code": "#include <iostream>\n#include <thread>\n#include <mutex>\n#include <condition_variable>\n#include <queue>\nusing namespace std;\n\nqueue<int> buffer;\nmutex mtx;\ncondition_variable cv;\nbool done = false;\n\nvoid producer() {\n    for (int i = 0; i < 5; i++) {\n        {\n            lock_guard<mutex> lock(mtx);\n            buffer.push(i);\n            cout << \"Produced: \" << i << endl;\n        }\n        cv.notify_one();\n    }\n    { lock_guard<mutex> lock(mtx); done = true; }\n    cv.notify_all();\n}\n\nvoid consumer() {\n    while (true) {\n        unique_lock<mutex> lock(mtx);\n        cv.wait(lock, [] { return !buffer.empty() || done; });\n        while (!buffer.empty()) {\n            cout << \"Consumed: \" << buffer.front() << endl;\n            buffer.pop();\n        }\n        if (done) break;\n    }\n}\n\nint main() {\n    thread p(producer), c(consumer);\n    p.join(); c.join();\n    return 0;\n}",
                "explanation": "Producer-consumer is a classic concurrency pattern. condition_variable with predicate handles spurious wakeups correctly."}],
             "commonMistakes": ["Not using a predicate with cv.wait() (spurious wakeups!)", "Using atomic for complex operations that need multiple steps (use mutex instead)"],
             "interviewTips": ["Know when to use atomic vs mutex (single variable vs compound operations)", "Explain memory ordering: seq_cst vs relaxed vs acquire/release"]}
        ],
        "quizQuestions": [
            {"id": "q9.1", "type": "multiple_choice", "difficulty": "medium",
             "question": "What happens if you don't call join() or detach() on a std::thread before it's destroyed?", "code": "",
             "options": ["Thread continues running", "Thread is silently joined", "std::terminate() is called", "Undefined behavior"],
             "correctAnswer": "std::terminate() is called",
             "explanation": "If a joinable thread's destructor runs, it calls std::terminate(). Always join or detach."},
            {"id": "q9.2", "type": "multiple_choice", "difficulty": "hard",
             "question": "Why should you always use a predicate with condition_variable::wait()?", "code": "",
             "options": ["For better performance", "To prevent spurious wakeups from causing bugs", "It's required by the standard", "To avoid deadlocks"],
             "correctAnswer": "To prevent spurious wakeups from causing bugs",
             "explanation": "Condition variables can wake up spuriously (without notify). The predicate re-checks the actual condition."},
            {"id": "q9.3", "type": "multiple_choice", "difficulty": "medium",
             "question": "Which C++17 feature locks multiple mutexes without risking deadlock?", "code": "",
             "options": ["lock_guard", "unique_lock", "scoped_lock", "recursive_mutex"],
             "correctAnswer": "scoped_lock",
             "explanation": "std::scoped_lock uses a deadlock avoidance algorithm to lock multiple mutexes safely."},
            {"id": "q9.4", "type": "true_false", "difficulty": "easy",
             "question": "True or False: std::atomic operations require a mutex for thread safety.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "False",
             "explanation": "atomic operations are lock-free and thread-safe by themselves. That's their purpose — avoiding mutexes for simple operations."}
        ]
    }

def chapter_modern_cpp():
    return {
        "id": 10, "title": "Modern C++ Features (C++11/14/17/20)", "slug": "modern-cpp",
        "description": "auto, structured bindings, optional/variant, string_view, constexpr, and other essential modern features.",
        "icon": "✨", "difficulty": "intermediate",
        "topics": [
            {"id": "10.1", "title": "auto, decltype, and Structured Bindings",
             "explanation": "auto deduces types from initializers. decltype gives the declared type of an expression. Structured bindings (C++17) decompose structs/pairs/tuples into named variables.",
             "keyPoints": ["auto x = 5; // int. auto& r = x; // int&", "decltype(expr) gives the type of expr without evaluating it", "auto in return types (C++14): auto func() { return 42; }", "Structured bindings: auto [x, y] = make_pair(1, 2);", "auto with const/references: const auto& is common for range-based for"],
             "codeExamples": [{"title": "Modern Type Deduction", "language": "cpp",
                "code": "#include <iostream>\n#include <map>\n#include <tuple>\nusing namespace std;\n\nauto add(int a, int b) { return a + b; } // C++14\n\nint main() {\n    auto x = 42;          // int\n    auto pi = 3.14;       // double\n    auto s = string(\"hi\"); // string\n\n    // Structured bindings (C++17)\n    auto [a, b] = make_pair(10, 20);\n    cout << a << \", \" << b << endl;  // 10, 20\n\n    // With maps\n    map<string, int> m = {{\"x\", 1}, {\"y\", 2}};\n    for (const auto& [key, val] : m)\n        cout << key << \"=\" << val << \" \";\n    cout << endl;\n\n    // Tuple decomposition\n    auto [name, age, gpa] = make_tuple(\"Alice\", 25, 3.9);\n    cout << name << \" age \" << age << endl;\n\n    return 0;\n}",
                "explanation": "auto and structured bindings make code cleaner without sacrificing type safety — types are still statically determined."}],
             "commonMistakes": ["auto x = {1}; deduces initializer_list in C++11 but int in C++17 for auto x{1}", "Forgetting & with auto in range-for (copies instead of references)"],
             "interviewTips": ["Know when auto is appropriate vs explicit types", "Explain that auto is a compile-time feature — no runtime cost"]},
            {"id": "10.2", "title": "std::optional, std::variant, std::string_view",
             "explanation": "optional<T>: May or may not hold a value (replaces nullable pointers/sentinel values).\nvariant<Types...>: Type-safe union (replaces C unions).\nstring_view: Non-owning view of a string (zero-copy).",
             "keyPoints": ["optional: has_value(), value(), value_or(default)", "variant: holds one of several types, visited with std::visit", "string_view: lightweight, non-owning reference to string data", "string_view avoids copies when passing substrings or string literals", "Never store string_view that outlives the underlying string"],
             "codeExamples": [{"title": "Optional, Variant, StringView", "language": "cpp",
                "code": "#include <iostream>\n#include <optional>\n#include <variant>\n#include <string_view>\nusing namespace std;\n\noptional<int> findIndex(const vector<int>& v, int target) {\n    for (int i = 0; i < v.size(); i++)\n        if (v[i] == target) return i;\n    return nullopt;  // Not found\n}\n\nint main() {\n    // Optional\n    vector<int> v = {1, 2, 3};\n    auto idx = findIndex(v, 2);\n    if (idx) cout << \"Found at: \" << *idx << endl;\n    cout << findIndex(v, 9).value_or(-1) << endl; // -1\n\n    // Variant (type-safe union)\n    variant<int, double, string> val = \"hello\";\n    cout << get<string>(val) << endl;\n    val = 42;  // Now holds int\n    visit([](auto& v) { cout << v << endl; }, val);\n\n    // String_view (zero-copy string reference)\n    string s = \"Hello World\";\n    string_view sv = s;\n    string_view sub = sv.substr(6, 5);  // \"World\" — no copy!\n    cout << sub << endl;\n\n    return 0;\n}",
                "explanation": "These types replace error-prone C patterns: optional vs NULL pointers, variant vs unions, string_view vs const char*."}],
             "commonMistakes": ["Storing string_view that outlives the source string (dangling)", "Using get<T> on variant without checking which type it holds (throws bad_variant_access)"],
             "interviewTips": ["Know the difference between optional and nullable pointer", "Explain when string_view is safe vs dangerous"]}
        ],
        "quizQuestions": [
            {"id": "q10.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "What does auto [a, b] = make_pair(1, 2); do?", "code": "",
             "options": ["Creates a pair", "Decomposes a pair into variables a and b", "Compilation error", "Creates two pairs"],
             "correctAnswer": "Decomposes a pair into variables a and b",
             "explanation": "Structured bindings (C++17) decompose aggregate types into named variables."},
            {"id": "q10.2", "type": "true_false", "difficulty": "medium",
             "question": "True or False: std::string_view owns the string data it refers to.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "False",
             "explanation": "string_view is a non-owning reference. The underlying string must outlive the string_view."},
            {"id": "q10.3", "type": "multiple_choice", "difficulty": "medium",
             "question": "What does std::optional<int> return when the value is absent?", "code": "",
             "options": ["0", "nullptr", "nullopt", "Throws exception"],
             "correctAnswer": "nullopt",
             "explanation": "nullopt represents the absence of a value in an optional. has_value() returns false."},
            {"id": "q10.4", "type": "multiple_choice", "difficulty": "hard",
             "question": "What is the advantage of std::variant over a C union?", "code": "",
             "options": ["Smaller memory footprint", "Type safety — tracks which type is active", "Faster access", "Supports member functions"],
             "correctAnswer": "Type safety — tracks which type is active",
             "explanation": "variant knows which type it currently holds and throws bad_variant_access if you access the wrong type. C unions have no such safety."}
        ]
    }

def chapter_type_casting():
    return {
        "id": 11, "title": "Type Casting & Type System", "slug": "type-casting",
        "description": "static_cast, dynamic_cast, const_cast, reinterpret_cast, and strict aliasing.",
        "icon": "🔄", "difficulty": "intermediate",
        "topics": [
            {"id": "11.1", "title": "C++ Cast Operators",
             "explanation": "C++ provides four explicit casts, each with specific semantics:\n- static_cast: compile-time checked conversions (numeric, up/downcasts)\n- dynamic_cast: runtime-checked polymorphic downcasts\n- const_cast: adds/removes const qualifier\n- reinterpret_cast: bit-pattern reinterpretation (dangerous)",
             "keyPoints": ["static_cast: most common, compile-time type checking", "dynamic_cast: requires virtual functions, returns nullptr on failure (pointers) or throws bad_cast (references)", "const_cast: only cast that can remove const; UB if object was originally const", "reinterpret_cast: type-punning, pointer to integer conversions", "Prefer C++ casts over C-style (T)x — they're searchable and explicit"],
             "codeExamples": [{"title": "Four C++ Casts", "language": "cpp",
                "code": "#include <iostream>\nusing namespace std;\n\nclass Base { public: virtual ~Base() {} };\nclass Derived : public Base { public: void special() { cout << \"Derived!\\n\"; } };\n\nint main() {\n    // static_cast: numeric conversion\n    double pi = 3.14;\n    int truncated = static_cast<int>(pi);  // 3\n\n    // dynamic_cast: safe downcast\n    Base* bp = new Derived();\n    Derived* dp = dynamic_cast<Derived*>(bp);\n    if (dp) dp->special();  // \"Derived!\"\n\n    Base* bp2 = new Base();\n    Derived* dp2 = dynamic_cast<Derived*>(bp2);\n    if (!dp2) cout << \"Cast failed safely\\n\";\n\n    // const_cast: remove const for legacy C API\n    const char* msg = \"hello\";\n    char* writable = const_cast<char*>(msg);\n    // WARNING: modifying *writable is UB since original is const!\n\n    // reinterpret_cast: raw memory interpretation\n    int val = 42;\n    char* bytes = reinterpret_cast<char*>(&val);\n    cout << \"First byte: \" << (int)bytes[0] << endl;\n\n    delete bp; delete bp2;\n    return 0;\n}",
                "explanation": "Each cast serves a specific purpose. Use the weakest cast that works to maximize safety."}],
             "commonMistakes": ["Using reinterpret_cast when static_cast would work", "Using dynamic_cast on non-polymorphic types (no virtual functions)", "Modifying through const_cast when original was actually const (UB)"],
             "interviewTips": ["Explain when each cast should be used", "Know that dynamic_cast has runtime overhead (RTTI)", "Understand strict aliasing rule and how reinterpret_cast can violate it"]}
        ],
        "quizQuestions": [
            {"id": "q11.1", "type": "multiple_choice", "difficulty": "medium",
             "question": "Which cast should you use for a safe downcast in an inheritance hierarchy?", "code": "",
             "options": ["static_cast", "dynamic_cast", "reinterpret_cast", "const_cast"],
             "correctAnswer": "dynamic_cast",
             "explanation": "dynamic_cast performs a runtime check and returns nullptr if the cast fails, making it safe for downcasting."},
            {"id": "q11.2", "type": "multiple_choice", "difficulty": "hard",
             "question": "What does dynamic_cast return when a pointer cast fails?", "code": "",
             "options": ["Throws bad_cast", "Returns nullptr", "Returns the base pointer", "Undefined behavior"],
             "correctAnswer": "Returns nullptr",
             "explanation": "For pointer casts, dynamic_cast returns nullptr on failure. For reference casts, it throws std::bad_cast."},
            {"id": "q11.3", "type": "true_false", "difficulty": "medium",
             "question": "True or False: C-style casts are preferred over C++ named casts in modern code.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "False",
             "explanation": "C++ named casts are preferred: they're explicit, searchable (grep), and each has specific semantics. C-style casts can silently perform dangerous conversions."}
        ]
    }

def chapter_error_handling():
    return {
        "id": 12, "title": "Error Handling & Exceptions", "slug": "error-handling",
        "description": "Exception hierarchy, noexcept, exception safety guarantees, and RAII for exception safety.",
        "icon": "🛡️", "difficulty": "intermediate",
        "topics": [
            {"id": "12.1", "title": "Exceptions and noexcept",
             "explanation": "C++ exceptions unwind the stack, calling destructors for all local objects (RAII). noexcept specifier indicates a function won't throw — enables optimizations and is required for move operations used with containers.",
             "keyPoints": ["throw expression creates and throws an exception object", "catch blocks handle exceptions by type, catch(...) catches all", "Stack unwinding calls destructors for all local objects", "noexcept functions call std::terminate if they throw", "Move constructors MUST be noexcept for optimal vector performance", "Exception safety levels: nothrow, strong, basic"],
             "codeExamples": [{"title": "Exception Safety with RAII", "language": "cpp",
                "code": "#include <iostream>\n#include <stdexcept>\n#include <vector>\nusing namespace std;\n\nclass Resource {\npublic:\n    Resource() { cout << \"Acquired\\n\"; }\n    ~Resource() { cout << \"Released\\n\"; }  // Always called!\n};\n\nvoid riskyOperation() {\n    Resource r;  // RAII: will be cleaned up even if we throw\n    vector<int> v(10);\n    throw runtime_error(\"Something went wrong\");\n    // r's destructor is called during stack unwinding\n    // v's destructor frees its memory\n}\n\nint main() {\n    try {\n        riskyOperation();\n    } catch (const runtime_error& e) {\n        cout << \"Caught: \" << e.what() << endl;\n    } catch (...) {\n        cout << \"Unknown exception\\n\";\n    }\n    return 0;\n}",
                "explanation": "RAII + exceptions = automatic cleanup. Resource r is always released, even when an exception is thrown."}],
             "commonMistakes": ["Throwing in destructors (terminates the program during stack unwinding)", "Not catching by const reference (slicing or unnecessary copies)", "Forgetting noexcept on move operations"],
             "interviewTips": ["Know the three exception safety guarantees: basic (no leaks), strong (rollback), nothrow", "Explain why destructors must be noexcept", "Discuss error codes vs exceptions tradeoffs (Ericsson/Qualcomm embedded contexts may prefer error codes)"]}
        ],
        "quizQuestions": [
            {"id": "q12.1", "type": "multiple_choice", "difficulty": "medium",
             "question": "What happens if a noexcept function throws an exception?", "code": "",
             "options": ["Exception is silently ignored", "std::terminate() is called", "Exception propagates normally", "Compilation error"],
             "correctAnswer": "std::terminate() is called",
             "explanation": "If a noexcept function throws, std::terminate() is called immediately. The exception does not propagate."},
            {"id": "q12.2", "type": "multiple_choice", "difficulty": "hard",
             "question": "Which exception safety guarantee means the operation either succeeds completely or has no effect?", "code": "",
             "options": ["Basic guarantee", "Strong guarantee", "Nothrow guarantee", "Weak guarantee"],
             "correctAnswer": "Strong guarantee",
             "explanation": "Strong guarantee = commit or rollback. The operation either completes fully or leaves the state unchanged. copy-and-swap idiom provides this."},
            {"id": "q12.3", "type": "true_false", "difficulty": "easy",
             "question": "True or False: Exceptions should be caught by const reference.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "True",
             "explanation": "Catching by const reference avoids slicing (if catching a base class) and unnecessary copies."}
        ]
    }

def chapter_preprocessor():
    return {
        "id": 13, "title": "Preprocessor & Compilation", "slug": "preprocessor-compilation",
        "description": "Macros, include guards, compilation stages, linking, ODR, and translation units.",
        "icon": "🔨", "difficulty": "intermediate",
        "topics": [
            {"id": "13.1", "title": "Macros, Include Guards, and Compilation Pipeline",
             "explanation": "The C/C++ build process: Preprocessing (#include, #define expansion) → Compilation (source to object) → Assembly → Linking (object files + libraries → executable).\n\nMacros are text substitution. Include guards (#ifndef/#define/#endif) or #pragma once prevent multiple inclusion.",
             "keyPoints": ["Preprocessor: text substitution before compilation", "Include guards prevent multiple definitions from multiple #include", "#pragma once is non-standard but universally supported and simpler", "Macros don't respect scope or types — prefer constexpr/inline/templates", "ODR: One Definition Rule — each entity defined exactly once across all TUs", "inline functions/variables (C++17) are exempt from ODR across TUs"],
             "codeExamples": [{"title": "Build Pipeline & Macros", "language": "cpp",
                "code": "// myheader.h\n#pragma once  // or: #ifndef MYHEADER_H / #define MYHEADER_H / #endif\n\n// Prefer constexpr over #define\nconstexpr int MAX_SIZE = 100;   // type-safe, scoped\n// #define MAX_SIZE 100         // old C way, no type safety\n\n// Prefer inline functions over macros\ninline int square(int x) { return x * x; }  // type-safe\n// #define SQUARE(x) ((x) * (x))  // dangerous: SQUARE(i++) double-evaluates\n\n// Sometimes macros are useful\n#define LOG(msg) std::cout << __FILE__ << \":\" << __LINE__ << \": \" << msg << std::endl\n\n// Conditional compilation (platform-specific code)\n#ifdef _WIN32\n    #define EXPORT __declspec(dllexport)\n#else\n    #define EXPORT __attribute__((visibility(\"default\")))\n#endif",
                "explanation": "Modern C++ replaces most macro uses with constexpr, inline, and templates. Use macros only for conditional compilation and debug logging."}],
             "commonMistakes": ["Macro arguments not parenthesized: #define MUL(a,b) a*b → MUL(1+2,3) = 1+2*3 = 7", "Forgetting include guards (multiple definition errors)", "Defining non-inline functions in headers (ODR violation)"],
             "interviewTips": ["Explain the full compilation pipeline for a C++ program", "Know the difference between compile-time and link-time errors", "Understand why templates must be in headers"]}
        ],
        "quizQuestions": [
            {"id": "q13.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "What is the purpose of #pragma once?", "code": "",
             "options": ["Optimize compilation", "Prevent multiple inclusion of a header", "Enable parallel compilation", "Define a macro"],
             "correctAnswer": "Prevent multiple inclusion of a header",
             "explanation": "#pragma once ensures a header file is included at most once per translation unit, preventing redefinition errors."},
            {"id": "q13.2", "type": "multiple_choice", "difficulty": "medium",
             "question": "What macro pitfall exists in: #define SQUARE(x) x * x", "code": "int result = SQUARE(1 + 2);",
             "options": ["No issue", "Result is 9", "Result is 5 due to operator precedence", "Compilation error"],
             "correctAnswer": "Result is 5 due to operator precedence",
             "explanation": "SQUARE(1+2) expands to 1+2 * 1+2 = 1+2+2 = 5. Fix: #define SQUARE(x) ((x) * (x))"},
            {"id": "q13.3", "type": "multiple_choice", "difficulty": "medium",
             "question": "In which compilation stage does #include expansion happen?", "code": "",
             "options": ["Compilation", "Preprocessing", "Linking", "Assembly"],
             "correctAnswer": "Preprocessing",
             "explanation": "The preprocessor handles all # directives (include, define, ifdef) before the compiler sees the code."}
        ]
    }

def chapter_storage():
    return {
        "id": 14, "title": "Storage Classes & Linkage", "slug": "storage-linkage",
        "description": "static, extern, mutable, thread_local, storage duration, and linkage types.",
        "icon": "📋", "difficulty": "intermediate",
        "topics": [
            {"id": "14.1", "title": "Storage Duration & Linkage",
             "explanation": "Storage duration: automatic (stack), static (global/static), dynamic (heap), thread (thread_local).\nLinkage: no linkage (local), internal (static/anonymous namespace), external (extern).",
             "keyPoints": ["static local: initialized once, persists across calls", "static global/function: internal linkage (file-scoped)", "extern: external linkage, declaration without definition", "thread_local: each thread gets its own copy", "mutable: allows modification in const member functions", "Anonymous namespace is the C++ way to get internal linkage (preferred over static)"],
             "codeExamples": [{"title": "Storage Classes Demo", "language": "cpp",
                "code": "#include <iostream>\n#include <thread>\nusing namespace std;\n\nint globalVar = 10;           // external linkage, static duration\nstatic int fileVar = 20;      // internal linkage, static duration\n\nvoid counter() {\n    static int count = 0;     // static local: persists across calls\n    cout << \"Call #\" << ++count << endl;\n}\n\nthread_local int tlVar = 0;   // each thread has its own copy\n\nvoid threadFunc(int id) {\n    tlVar = id;\n    cout << \"Thread \" << id << \": tlVar = \" << tlVar << endl;\n}\n\nclass Config {\n    mutable int accessCount_ = 0; // mutable: modifiable in const methods\n    int value_;\npublic:\n    Config(int v) : value_(v) {}\n    int getValue() const {\n        accessCount_++;  // OK because mutable\n        return value_;\n    }\n};\n\nint main() {\n    counter(); counter(); counter(); // Call #1, #2, #3\n    thread t1(threadFunc, 1), t2(threadFunc, 2);\n    t1.join(); t2.join();\n    return 0;\n}",
                "explanation": "Each storage class and qualifier serves a specific purpose. static local is the most commonly asked about in interviews."}],
             "commonMistakes": ["Confusing static at file scope (internal linkage) with static in a class (shared member)", "Forgetting that static locals are initialized only once (not thread-safe before C++11)"],
             "interviewTips": ["Explain the Meyers Singleton: static local with lazy initialization", "Know that C++11 guarantees thread-safe initialization of static locals"]}
        ],
        "quizQuestions": [
            {"id": "q14.1", "type": "multiple_choice", "difficulty": "easy",
             "question": "How many times is a static local variable initialized?", "code": "",
             "options": ["Every function call", "Once, on first call", "Once, at program start", "Depends on the compiler"],
             "correctAnswer": "Once, on first call",
             "explanation": "Static local variables are initialized the first time execution reaches their declaration. In C++11+, this is thread-safe."},
            {"id": "q14.2", "type": "multiple_choice", "difficulty": "medium",
             "question": "What does the mutable keyword allow?", "code": "",
             "options": ["Variable can change type", "Member can be modified in const methods", "Variable is thread-safe", "Variable is allocated on heap"],
             "correctAnswer": "Member can be modified in const methods",
             "explanation": "mutable lets a data member be modified even in const member functions. Used for caches, mutexes, debug counters."},
            {"id": "q14.3", "type": "multiple_choice", "difficulty": "medium",
             "question": "What does thread_local guarantee?", "code": "",
             "options": ["Variable is mutex-protected", "Each thread has its own copy of the variable", "Variable is atomic", "Variable is allocated on the stack"],
             "correctAnswer": "Each thread has its own copy of the variable",
             "explanation": "thread_local creates a separate instance of the variable for each thread, avoiding shared state."}
        ]
    }

def chapter_ub():
    return {
        "id": 15, "title": "Undefined Behavior & Pitfalls", "slug": "undefined-behavior",
        "description": "Common sources of undefined behavior and dangerous patterns every C/C++ developer must know.",
        "icon": "⚠️", "difficulty": "advanced",
        "topics": [
            {"id": "15.1", "title": "Common Sources of Undefined Behavior",
             "explanation": "Undefined behavior (UB) means the C/C++ standard places NO requirements on the program's behavior. Compilers may optimize assuming UB never occurs, leading to surprising results.\n\nMost security vulnerabilities in C/C++ stem from UB: buffer overflows, use-after-free, null dereference.",
             "keyPoints": ["Signed integer overflow is UB (unsigned wraps around)", "Dereferencing null or dangling pointers", "Buffer overflow: accessing beyond array bounds", "Use-after-free and double-free", "Shifting by >= bit width of the type", "Reading uninitialized variables", "Modifying a const object through const_cast", "Data races: unsynchronized concurrent access to shared data", "Violating strict aliasing rule"],
             "codeExamples": [{"title": "Common UB Examples", "language": "cpp",
                "code": "#include <iostream>\n#include <climits>\nusing namespace std;\n\nint main() {\n    // 1. Signed overflow (UB!) — compiler may optimize this away\n    int x = INT_MAX;\n    // if (x + 1 > x)  // Compiler may assume this is always true!\n\n    // 2. Buffer overflow (UB!)\n    int arr[5];\n    // arr[10] = 42;  // Writing beyond bounds\n\n    // 3. Use after free (UB!)\n    int *p = new int(42);\n    delete p;\n    // *p = 10;  // Dangling pointer access\n\n    // 4. Null dereference (UB!)\n    int *null = nullptr;\n    // *null = 5;  // Crash or worse\n\n    // 5. Uninitialized read (UB!)\n    int uninit;\n    // cout << uninit;  // Could be anything\n\n    // 6. Shift overflow (UB!)\n    // int shifted = 1 << 32;  // UB for 32-bit int\n\n    cout << \"No UB triggered in this run!\" << endl;\n    return 0;\n}",
                "explanation": "UB makes programs unpredictable. Compilers exploit UB for optimization — a signed overflow check may be removed entirely."}],
             "commonMistakes": ["Assuming signed integer overflow wraps like unsigned", "Assuming UB will crash — it might 'work' today and fail tomorrow", "Not using sanitizers (ASan, UBSan) during development"],
             "interviewTips": ["Know at least 5-6 sources of UB by heart", "Explain why compilers exploit UB for optimization", "Mention sanitizers: -fsanitize=address,undefined"]}
        ],
        "quizQuestions": [
            {"id": "q15.1", "type": "multiple_choice", "difficulty": "medium",
             "question": "Which of the following is undefined behavior?", "code": "",
             "options": ["unsigned int overflow", "Signed int overflow", "Float to int truncation", "Integer division (non-zero divisor)"],
             "correctAnswer": "Signed int overflow",
             "explanation": "Signed integer overflow is UB. Unsigned overflow wraps around (well-defined). Float truncation is well-defined. Division by non-zero is fine."},
            {"id": "q15.2", "type": "true_false", "difficulty": "hard",
             "question": "True or False: If a program has undefined behavior, the compiler is allowed to do ANYTHING, including formatting your hard drive.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "True",
             "explanation": "Technically correct per the standard. In practice, compilers usually just optimize aggressively, but UB means NO guarantees whatsoever."},
            {"id": "q15.3", "type": "multiple_choice", "difficulty": "medium",
             "question": "What tool helps detect undefined behavior at runtime?", "code": "",
             "options": ["Valgrind only", "GDB", "UBSan (-fsanitize=undefined)", "Lint"],
             "correctAnswer": "UBSan (-fsanitize=undefined)",
             "explanation": "UBSan is a compiler sanitizer that detects undefined behavior at runtime with minimal overhead. Use with -fsanitize=undefined."}
        ]
    }

def chapter_systems():
    return {
        "id": 16, "title": "Systems Programming Essentials", "slug": "systems-programming",
        "description": "volatile, IPC, signal handling, sockets, and cache — essential for telecom/embedded roles at Ericsson/Qualcomm.",
        "icon": "🖥️", "difficulty": "advanced",
        "topics": [
            {"id": "16.1", "title": "volatile, IPC & Sockets",
             "explanation": "volatile tells the compiler the value may change outside the program's control (hardware registers, signal handlers, memory-mapped I/O). It prevents optimization of reads/writes.\n\nIPC mechanisms: pipes, shared memory, message queues, sockets, signals. Sockets are the foundation of network programming in telecom.",
             "keyPoints": ["volatile prevents compiler from caching variable in register", "volatile does NOT provide atomicity or thread safety (use atomic for that)", "Sockets: AF_INET + SOCK_STREAM (TCP) or SOCK_DGRAM (UDP)", "Shared memory: fastest IPC, but requires synchronization", "Signals: asynchronous notifications (SIGINT, SIGTERM, SIGUSR1)", "In telecom: socket programming is essential for protocol stacks"],
             "codeExamples": [{"title": "Volatile and Socket Basics", "language": "cpp",
                "code": "// volatile: hardware register access (embedded/telecom)\nvolatile uint32_t* const HW_REG = (volatile uint32_t*)0x40001000;\n// *HW_REG = 0x01;  // Write to hardware register\n// uint32_t status = *HW_REG;  // Read — compiler won't optimize away\n\n// Basic TCP client (POSIX)\n#include <sys/socket.h>\n#include <netinet/in.h>\n#include <unistd.h>\n#include <cstring>\n\nvoid tcpClient() {\n    int sock = socket(AF_INET, SOCK_STREAM, 0);\n    struct sockaddr_in server;\n    server.sin_family = AF_INET;\n    server.sin_port = htons(8080);  // Network byte order!\n    server.sin_addr.s_addr = inet_addr(\"127.0.0.1\");\n\n    connect(sock, (struct sockaddr*)&server, sizeof(server));\n\n    const char* msg = \"Hello Server\";\n    send(sock, msg, strlen(msg), 0);\n\n    char buffer[1024] = {0};\n    recv(sock, buffer, sizeof(buffer), 0);\n\n    close(sock);\n}",
                "explanation": "volatile is for hardware/signal handlers, NOT threading. Sockets are the foundation of telecom network stacks."}],
             "commonMistakes": ["Using volatile for thread safety (it's not atomic!)", "Not converting byte order with htons/htonl for network communication", "Forgetting to close sockets (resource leak)"],
             "interviewTips": ["Ericsson/Nokia/Qualcomm will ask about socket programming and protocol stacks", "Know select/poll/epoll for handling multiple connections", "Explain the difference between TCP and UDP for telecom applications", "Know volatile vs atomic: volatile prevents optimization, atomic provides thread safety"]}
        ],
        "quizQuestions": [
            {"id": "q16.1", "type": "true_false", "difficulty": "medium",
             "question": "True or False: volatile provides thread safety for shared variables.", "code": "",
             "options": ["True", "False"],
             "correctAnswer": "False",
             "explanation": "volatile only prevents compiler optimization. It does NOT provide atomicity or memory ordering. Use std::atomic for thread safety."},
            {"id": "q16.2", "type": "multiple_choice", "difficulty": "medium",
             "question": "Which function converts host byte order to network byte order for a 16-bit value?", "code": "",
             "options": ["htonl()", "htons()", "ntohl()", "ntohs()"],
             "correctAnswer": "htons()",
             "explanation": "htons = Host TO Network Short (16-bit). htonl is for 32-bit. ntohs/ntohl are the reverse conversions."},
            {"id": "q16.3", "type": "multiple_choice", "difficulty": "hard",
             "question": "Which IPC mechanism is fastest for inter-process communication on the same machine?", "code": "",
             "options": ["TCP sockets", "Named pipes", "Shared memory", "Message queues"],
             "correctAnswer": "Shared memory",
             "explanation": "Shared memory avoids kernel-mediated copies. Data is directly accessible by both processes. Requires explicit synchronization (semaphores/mutexes)."}
        ]
    }


def build_cpp_concepts():
    data = {
        "metadata": {
            "title": "C/C++ Mastery Guide for Senior Engineers",
            "description": "Comprehensive C/C++ concepts covering pointers, memory management, bit manipulation, OOP, templates, STL, concurrency, and modern C++ features. Designed for senior engineers preparing for roles at Nvidia, Google, Qualcomm, Ericsson, and Arista Networks.",
            "version": "1.0",
            "targetAudience": "Senior Software Engineers (5+ years) refreshing C/C++ for big tech interviews",
            "targetCompanies": ["Nvidia", "Google", "Qualcomm", "Ericsson", "Arista Networks", "Nokia", "Samsung", "Intel", "AMD", "Apple"],
            "totalChapters": 16,
            "generatedDate": "2026-06-23",
            "features": ["Detailed explanations", "Code examples", "Common mistakes", "Interview tips", "Quiz questions"]
        },
        "chapters": [
            chapter_pointers(),
            chapter_smart_pointers(),
            chapter_memory(),
            chapter_bit_manipulation(),
            chapter_classes_oop(),
            chapter_templates(),
            chapter_stl_containers(),
            chapter_stl_algorithms(),
            chapter_concurrency(),
            chapter_modern_cpp(),
            chapter_type_casting(),
            chapter_error_handling(),
            chapter_preprocessor(),
            chapter_storage(),
            chapter_ub(),
            chapter_systems()
        ]
    }
    return data

if __name__ == "__main__":
    data = build_cpp_concepts()
    output_path = os.path.join(r"C:\GitHub\Focus", "cpp_concepts.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    total_topics = sum(len(ch["topics"]) for ch in data["chapters"])
    total_quizzes = sum(len(ch["quizQuestions"]) for ch in data["chapters"])
    total_examples = sum(
        sum(len(t.get("codeExamples", [])) for t in ch["topics"])
        for ch in data["chapters"]
    )
    print(f"Generated {output_path}")
    print(f"  Chapters: {len(data['chapters'])}")
    print(f"  Topics: {total_topics}")
    print(f"  Code Examples: {total_examples}")
    print(f"  Quiz Questions: {total_quizzes}")
