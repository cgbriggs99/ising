	.file	"ising.c"
	.text
	.globl	__popcountdi2
	.p2align 4,,15
	.type	compute_vals, @function
compute_vals:
.LFB19:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$72, %rsp
	.cfi_def_cfa_offset 128
	movl	(%rdi), %eax
	movl	%eax, %ebx
	movl	%eax, 60(%rsp)
	movl	12(%rdi), %eax
	cmpl	%ebx, %eax
	jle	.L2
	movl	8(%rdi), %r14d
	movq	%rdi, %r12
	movl	$1, %ebx
	.p2align 4,,10
	.p2align 3
.L3:
	movslq	60(%rsp), %r13
	movl	%ebx, %esi
	movl	%r14d, %ecx
	sall	%cl, %esi
	testl	%esi, %esi
	leaq	0(,%r13,8), %rbp
	jle	.L10
	xorl	%r15d, %r15d
	xorl	%eax, %eax
	movq	$0x000000000, 40(%rsp)
	movq	$0x000000000, 32(%rsp)
	movq	$0x000000000, 24(%rsp)
	movq	$0x000000000, 16(%rsp)
	jmp	.L5
	.p2align 4,,10
	.p2align 3
.L11:
	movq	%r15, %rdi
	call	__popcountdi2@PLT
.L5:
	pxor	%xmm1, %xmm1
	addl	%eax, %eax
	subl	%r14d, %eax
	leal	-1(%r14), %ecx
	movl	%r15d, %edi
	cvtsi2sd	%eax, %xmm1
	movl	%r15d, %eax
	sall	%cl, %edi
	sarl	%eax
	movl	%r14d, %ecx
	orl	%eax, %edi
	movl	%r15d, %eax
	notl	%eax
	xorl	%eax, %edi
	movq	$-1, %rax
	salq	%cl, %rax
	movslq	%edi, %rdi
	notq	%rax
	andq	%rax, %rdi
	movsd	%xmm1, 8(%rsp)
	call	__popcountdi2@PLT
	pxor	%xmm1, %xmm1
	addl	%eax, %eax
	subl	%r14d, %eax
	movsd	8(%rsp), %xmm0
	cvtsi2sd	%eax, %xmm1
	mulsd	24(%r12), %xmm0
	movq	40(%r12), %rax
	movsd	(%rax,%rbp), %xmm2
	mulsd	32(%r12), %xmm2
	mulsd	16(%r12), %xmm1
	addsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm3
	movsd	%xmm1, 48(%rsp)
	xorpd	.LC1(%rip), %xmm3
	movapd	%xmm3, %xmm0
	divsd	%xmm2, %xmm0
	call	exp@PLT
	movsd	48(%rsp), %xmm1
	movl	8(%r12), %r14d
	movsd	32(%rsp), %xmm5
	leal	1(%r15), %eax
	movapd	%xmm1, %xmm2
	mulsd	%xmm1, %xmm1
	movsd	16(%rsp), %xmm4
	movl	%ebx, %edx
	mulsd	%xmm0, %xmm2
	movl	%r14d, %ecx
	addq	$1, %r15
	addsd	%xmm0, %xmm4
	sall	%cl, %edx
	mulsd	%xmm0, %xmm1
	cmpl	%eax, %edx
	addsd	24(%rsp), %xmm2
	movsd	%xmm4, 16(%rsp)
	addsd	%xmm1, %xmm5
	movsd	8(%rsp), %xmm1
	mulsd	%xmm1, %xmm1
	movsd	%xmm2, 24(%rsp)
	movsd	%xmm5, 32(%rsp)
	mulsd	%xmm1, %xmm0
	addsd	40(%rsp), %xmm0
	movsd	%xmm0, 40(%rsp)
	jg	.L11
	movl	12(%r12), %eax
	movapd	%xmm2, %xmm0
	movapd	%xmm4, %xmm7
	movapd	%xmm5, %xmm1
.L6:
	divsd	%xmm7, %xmm0
	movq	48(%r12), %rcx
	movl	4(%r12), %edx
	addl	%edx, 60(%rsp)
	movl	60(%rsp), %esi
	cmpl	%eax, %esi
	divsd	%xmm7, %xmm1
	movsd	%xmm0, (%rcx,%r13,8)
	movq	56(%r12), %rcx
	mulsd	%xmm0, %xmm0
	subsd	%xmm0, %xmm1
	movsd	40(%rsp), %xmm0
	divsd	%xmm7, %xmm0
	movsd	%xmm1, (%rcx,%r13,8)
	movq	64(%r12), %rcx
	movsd	%xmm0, (%rcx,%r13,8)
	jl	.L3
.L2:
	addq	$72, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L10:
	.cfi_restore_state
	movq	$0x000000000, 32(%rsp)
	movq	$0x000000000, 24(%rsp)
	movq	$0x000000000, 16(%rsp)
	movq	$0x000000000, 40(%rsp)
	movsd	24(%rsp), %xmm0
	movsd	16(%rsp), %xmm7
	movsd	32(%rsp), %xmm1
	jmp	.L6
	.cfi_endproc
.LFE19:
	.size	compute_vals, .-compute_vals
	.p2align 4,,15
	.globl	threaded_ising
	.type	threaded_ising, @function
threaded_ising:
.LFB20:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$120, %rsp
	.cfi_def_cfa_offset 176
	movl	176(%rsp), %r12d
	movl	%edi, 32(%rsp)
	movsd	%xmm0, (%rsp)
	movq	%rsi, 24(%rsp)
	movl	$8, %esi
	movsd	%xmm1, 8(%rsp)
	movsd	%xmm2, 16(%rsp)
	movl	%edx, 36(%rsp)
	leal	-1(%r12), %r13d
	movq	%rcx, 40(%rsp)
	movq	%r8, 48(%rsp)
	movslq	%r13d, %rbx
	movq	%r9, 56(%rsp)
	movq	%rbx, %rdi
	movq	%fs:40, %rax
	movq	%rax, 104(%rsp)
	xorl	%eax, %eax
	call	calloc@PLT
	movq	%rbx, %rdi
	movl	$56, %esi
	movq	%rax, %rbp
	movq	%rax, 72(%rsp)
	call	calloc@PLT
	movslq	%r12d, %rdx
	movl	$72, %esi
	movq	%rax, %rbx
	movq	%rdx, %rdi
	movq	%rax, 88(%rsp)
	movq	%rdx, 80(%rsp)
	call	calloc@PLT
	testl	%r12d, %r12d
	movq	%rax, 64(%rsp)
	jle	.L13
	movq	%rax, %r15
	xorl	%r14d, %r14d
	.p2align 4,,10
	.p2align 3
.L14:
	movl	32(%rsp), %eax
	movsd	(%rsp), %xmm3
	movsd	8(%rsp), %xmm4
	cmpl	%r14d, %r13d
	movsd	16(%rsp), %xmm5
	movl	%r14d, (%r15)
	movl	%eax, 8(%r15)
	movl	36(%rsp), %eax
	movsd	%xmm3, 16(%r15)
	movl	%r12d, 4(%r15)
	movsd	%xmm4, 24(%r15)
	movsd	%xmm5, 32(%r15)
	movl	%eax, 12(%r15)
	movq	24(%rsp), %rax
	movq	%rax, 40(%r15)
	movq	40(%rsp), %rax
	movq	%rax, 48(%r15)
	movq	48(%rsp), %rax
	movq	%rax, 56(%r15)
	movq	56(%rsp), %rax
	movq	%rax, 64(%r15)
	je	.L15
	movq	%rbx, %rdi
	addl	$1, %r14d
	call	pthread_attr_init@PLT
	leaq	compute_vals(%rip), %rdx
	movq	%r15, %rcx
	movq	%rbx, %rsi
	movq	%rbp, %rdi
	addq	$72, %r15
	addq	$56, %rbx
	call	pthread_create@PLT
	addq	$8, %rbp
	cmpl	%r12d, %r14d
	jne	.L14
.L13:
	movq	80(%rsp), %rax
	movq	64(%rsp), %rcx
	leaq	(%rax,%rax,8), %rax
	leaq	-72(%rcx,%rax,8), %rdi
	call	compute_vals
	testl	%r13d, %r13d
	jle	.L17
	movq	72(%rsp), %rcx
	leal	-2(%r12), %eax
	leaq	96(%rsp), %rbp
	leaq	8(%rcx,%rax,8), %r12
	movq	%rcx, %rbx
	.p2align 4,,10
	.p2align 3
.L18:
	movq	(%rbx), %rdi
	movq	%rbp, %rsi
	addq	$8, %rbx
	call	pthread_join@PLT
	cmpq	%rbx, %r12
	jne	.L18
.L17:
	movq	64(%rsp), %rdi
	call	free@PLT
	movq	72(%rsp), %rdi
	call	free@PLT
	movq	88(%rsp), %rdi
	call	free@PLT
	xorl	%eax, %eax
	movq	104(%rsp), %rdx
	xorq	%fs:40, %rdx
	jne	.L22
	addq	$120, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L15:
	.cfi_restore_state
	leal	1(%r13), %r14d
	addq	$72, %r15
	addq	$56, %rbx
	addq	$8, %rbp
	cmpl	%r14d, %r12d
	jne	.L14
	jmp	.L13
.L22:
	call	__stack_chk_fail@PLT
	.cfi_endproc
.LFE20:
	.size	threaded_ising, .-threaded_ising
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC1:
	.long	0
	.long	-2147483648
	.long	0
	.long	0
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
