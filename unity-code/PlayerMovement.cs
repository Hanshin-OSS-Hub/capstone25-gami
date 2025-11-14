using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    Vector3 dirVec;
    [Header("이동 속도")]
    public float moveSpeed = 5f;

    public GameManager manager;
    GameObject scanObject;

    [Header("부위 SpriteRenderer들")]
    [SerializeField] private SpriteRenderer[] spriteRenderers; // head, body, hand 등

    [Header("손 Transform")]
    [SerializeField] private Transform hand; // Inspector에서 손 지정

    private Rigidbody2D rb;
    private Animator animator;
    private Vector2 moveInput;
    private bool facingRight = true;
    private float handOriginalX;
    
    // 상호작용 딜레이 변수
    public float actionDelay = 0.2f;
    private float nextActionTime = 0f;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        animator = GetComponent<Animator>();

        // 자동 할당: Inspector에 안 넣어도 Player 자식에 있는 모든 SpriteRenderer 가져오기
        if (spriteRenderers == null || spriteRenderers.Length == 0)
            spriteRenderers = GetComponentsInChildren<SpriteRenderer>();

        // 손 X 위치 저장
        if (hand != null)
            handOriginalX = hand.localPosition.x;
    }

    void Update()
    {
        // 이동 입력
        moveInput.x = manager.isAction? 0 : Input.GetAxisRaw("Horizontal");
        moveInput.y = manager.isAction? 0 : Input.GetAxisRaw("Vertical");

        // 이동 애니메이션
        bool isWalking = moveInput.magnitude > 0;
        animator.SetBool("isWalking", isWalking);
        animator.SetFloat("moveX", moveInput.x);
        animator.SetFloat("moveY", moveInput.y);

        // Flip 처리
        if (moveInput.x > 0 && !facingRight)
            Flip();
        else if (moveInput.x < 0 && facingRight)
            Flip();

        // Scan 시선 처리
        if (moveInput.y > 0)
            dirVec = Vector3.up;
        else if (moveInput.y < 0)
            dirVec = Vector3.down;
        else if (moveInput.x > 0)
            dirVec = Vector3.right;
        else if (moveInput.x < 0)
            dirVec = Vector3.left;


        //Scan Object
        if (Input.GetButton("Jump") && scanObject != null && Time.time >= nextActionTime)
        {
            //Debug.Log("This is : " + scanObject.name);
            manager.Action(scanObject);
            nextActionTime = Time.time + actionDelay;
            Debug.Log("spacebar test");
        }
            
    }

    void FixedUpdate()
    {
        // Detect
        //Debug.DrawRay(rb.position, dirVec * 0.7f, new Color(0, 1, 0)); 감지 범위 확인
        RaycastHit2D rayHit = Physics2D.Raycast(rb.position, dirVec, 0.7f, LayerMask.GetMask("Object"));

        if (rayHit.collider != null)
        {
            scanObject = rayHit.collider.gameObject;
        }
        else
            scanObject = null;

        // Rigidbody 이동
        rb.linearVelocity = moveInput.normalized * moveSpeed;
    }

void Flip()
{
    facingRight = !facingRight;

    foreach (var sr in spriteRenderers)
    {
        sr.flipX = !sr.flipX; // 손도 포함되어 있으면 자연스럽게 Flip
    }
}
}