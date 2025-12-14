        314 +    margin: 20px 0;
        315 +  }
        316 +
        317 +  .tlw-years {
        318 +    display: flex;
        319 +    flex-direction: column;
        320 +    align-items: center;
        321 +    min-width: 120px;
        322 +  }
        323 +
        324 +  .tlw-number {
        325 +    font-size: 72px;
        326 +    font-weight: 700;
        327 +    color: #9ca3af;
        328 +    line-height: 1;
        329 +  }
        330 +
        331 +  .tlw-unit {
        332 +    font-size: 18px;
        333 +    color: var(--muted);
        334 +    text-transform: uppercase;
        335 +    letter-spacing: 0.1em;
        336 +  }
        337 +
        338 +  .tlw-story h3 {
        339 +    margin: 0 0 8px;
        340 +    font-size: 28px;
        341 +  }
        342 +
        343 +  .tlw-dates {
        344 +    color: var(--muted);
        345 +    margin: 0 0 16px;
        346 +  }
        347 +
        348 +  .tlw-context {
        349 +    color: var(--text);
        350 +    line-height: 1.7;
        351 +    margin: 0;
        352 +  }
        353 +
        354 +  .tlw-timeline {
        355 +    margin: 32px 0;
        356 +    padding: 24px;
        357 +    background: rgba(0, 0, 0, 0.2);
        358 +    border-radius: 12px;
        359 +  }
        360 +
        361 +  .timeline-track {
        362 +    display: flex;
        363 +    flex-wrap: wrap;
        364 +    gap: 16px;
        365 +  }
        366 +
        367 +  .timeline-point {
        368 +    flex: 1;
        369 +    min-width: 100px;
        370 +    position: relative;
        371 +    padding-left: 20px;
        372 +  }
        373 +
        374 +  .timeline-point::before {
        375 +    content: '';
        376 +    position: absolute;
        377 +    left: 0;
        378 +    top: 0;
        379 +    bottom: 0;
        380 +    width: 2px;
        381 +    background: var(--border);
        382 +  }
        383 +
        384 +  .timeline-point.start .timeline-dot,
        385 +  .timeline-point.end .timeline-dot {
        386 +    background: var(--accent);
        387 +    width: 12px;
        388 +    height: 12px;
        389 +  }
        390 +
        391 +  .timeline-dot {
        392 +    position: absolute;
        393 +    left: -4px;
        394 +    top: 4px;
        395 +    width: 10px;
        396 +    height: 10px;
        397 +    background: var(--muted);
        398 +    border-radius: 50%;
        399 +  }
        400 +
        401 +  .timeline-content {
        402 +    display: flex;
        403 +    flex-direction: column;
        404 +    gap: 2px;
        405 +  }
        406 +
        407 +  .timeline-year {
        408 +    font-weight: 700;
        409 +    color: var(--accent);
        410 +  }
        411 +
        412    .timeline-label {
        413 -    dominant-baseline: central;
        414 -    text-anchor: middle;
        413 +    font-size: 13px;
        414 +    font-weight: 600;
        415    }
        416
        417 -  .timeline-meta {
        417 +  .timeline-detail {
        418 +    font-size: 12px;
        419 +    color: var(--muted);
        420 +  }
        421 +
        422 +  .long-waiters {
        423 +    margin-top: 32px;
        424 +  }
        425 +
        426 +  .long-waiters h4 {
        427 +    margin: 0 0 16px;
        428 +  }
        429 +
        430 +  .waiter-list {
        431      display: flex;
        432 -    gap: 20px;
        433 -    padding: 12px 20px 16px;
        432 +    flex-direction: column;
        433 +    gap: 12px;
        434 +  }
        435 +
        436 +  .waiter-row {
        437 +    display: flex;
        438 +    align-items: center;
        439 +    gap: 16px;
        440 +  }
        441 +
        442 +  .waiter-info {
        443 +    flex: 1;
        444 +    min-width: 200px;
        445 +  }
        446 +
        447 +  .waiter-name {
        448 +    font-weight: 600;
        449 +    display: block;
        450 +  }
        451 +
        452 +  .waiter-album {
        453 +    font-size: 12px;
        454 +    color: var(--muted);
        455 +  }
        456 +
        457 +  .waiter-years {
        458 +    flex: 2;
        459 +    display: flex;
        460 +    align-items: center;
        461 +    gap: 12px;
        462 +  }
        463 +
        464 +  .waiter-bar {
        465 +    height: 8px;
        466 +    background: var(--accent);
        467 +    border-radius: 4px;
        468 +  }
        469 +
        470 +  .waiter-value {
        471 +    font-size: 13px;
        472 +    font-weight: 600;
        473 +    min-width: 80px;
        474 +  }
        475 +
        476 +  .tlw-stats {
        477 +    display: flex;
        478 +    gap: 32px;
        479 +    margin-top: 32px;
        480 +    padding-top: 24px;
        481      border-top: 1px solid var(--border);
        482 +  }
        483 +
        484 +  .tlw-stat {
        485 +    text-align: center;
        486 +  }
        487 +
        488 +  .stat-number {
        489 +    display: block;
        490 +    font-size: 32px;
        491 +    font-weight: 700;
        492 +    color: var(--accent);
        493 +  }
        494 +
        495 +  .stat-desc {
        496 +    font-size: 12px;
        497 +    color: var(--muted);
        498 +  }
        499 +
        500 +  /* 2025 Tour Section */
        501 +  .tour-hero {
        502 +    padding: 24px;
        503 +    background: linear-gradient(135deg, #1c2333, #0f1115);
        504 +    border-radius: 12px;
        505 +    margin: 20px 0;
        506 +  }
        507 +
        508 +  .tour-stat-grid {
        509 +    display: flex;
        510 +    gap: 32px;
        511 +    margin-bottom: 16px;
        512 +  }
        513 +
        514 +  .tour-stat {
        515 +    text-align: center;
        516 +  }
        517 +
        518 +  .tour-number {
        519 +    display: block;
        520 +    font-size: 48px;
        521 +    font-weight: 700;
        522 +    color: var(--accent);
        523 +  }
        524 +
        525 +  .tour-label {
        526 +    font-size: 12px;
        527 +    color: var(--muted);
        528 +  }
        529 +
        530 +  .tour-context {
        531 +    color: var(--muted);
        532 +    line-height: 1.6;
        533 +    margin: 0;
        534 +  }
        535 +
        536 +  .era-distribution {
        537 +    margin: 24px 0;
        538 +  }
        539 +
        540 +  .era-distribution h4 {
        541 +    margin: 0 0 16px;
        542 +  }
        543 +
        544 +  .era-bars {
        545 +    display: flex;
        546 +    flex-direction: column;
        547 +    gap: 10px;
        548 +  }
        549 +
        550 +  .era-bar-row {
        551 +    display: grid;
        552 +    grid-template-columns: 100px 1fr 50px;
        553 +    gap: 12px;
        554 +    align-items: center;
        555 +  }
        556 +
        557 +  .era-name {
        558 +    font-weight: 600;
        559 +  }
        560 +
        561 +  .era-bar-track {
        562 +    height: 12px;
        563 +    background: rgba(0, 0, 0, 0.3);
        564 +    border-radius: 6px;
        565 +    overflow: hidden;
        566 +  }
        567 +
        568 +  .era-bar-fill {
        569 +    height: 100%;
        570 +    border-radius: 6px;
        571 +  }
        572 +
        573 +  .era-pct {
        574 +    font-size: 13px;
        575 +    font-weight: 600;
        576 +    text-align: right;
        577 +  }
        578 +
        579 +  .top-songs {
        580 +    margin: 24px 0;
        581 +  }
        582 +
        583 +  .top-songs h4 {
        584 +    margin: 0 0 16px;
        585 +  }
        586 +
        587 +  .song-grid {
        588 +    display: grid;
        589 +    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        590 +    gap: 10px;
        591 +  }
        592 +
        593 +  .song-card {
        594 +    display: flex;
        595 +    align-items: center;
        596 +    gap: 12px;
        597 +    padding: 12px;
        598 +    background: rgba(0, 0, 0, 0.2);
        599 +    border-radius: 8px;
        600 +  }
        601 +
        602 +  .song-rank {
        603 +    font-size: 18px;
        604 +    font-weight: 700;
        605 +    color: var(--accent);
        606 +    min-width: 28px;
        607 +  }
        608 +
        609 +  .song-title {
        610 +    font-weight: 600;
        611 +    font-size: 14px;
        612 +  }
        613 +
        614 +  .song-appearances {
        615 +    display: block;
        616 +    font-size: 12px;
        617 +    color: var(--muted);
        618 +  }
        619 +
        620 +  .complete-albums {
        621 +    margin: 24px 0;
        622 +  }
        623 +
        624 +  .complete-albums h4 {
        625 +    margin: 0 0 16px;
        626 +  }
        627 +
        628 +  .album-show-list {
        629 +    display: flex;
        630 +    flex-direction: column;
        631 +    gap: 8px;
        632 +  }
        633 +
        634 +  .album-show {
        635 +    display: grid;
        636 +    grid-template-columns: 100px 100px 1fr;
        637 +    gap: 16px;
        638 +    padding: 12px;
        639 +    background: rgba(0, 0, 0, 0.2);
        640 +    border-radius: 8px;
        641 +  }
        642 +
        643 +  .show-date {
        644 +    font-weight: 600;
        645 +  }
        646 +
        647 +  .show-city {
        648 +    color: var(--muted);
        649 +  }
        650 +
        651 +  .show-album {
        652 +    font-size: 14px;
        653 +  }
        654 +
        655 +  .tour-interpretation {
        656 +    padding: 20px;
        657      background: rgba(255, 255, 255, 0.02);
        658 +    border-radius: 12px;
        659 +    margin-top: 24px;
        660    }
        661
        662 -  .stat-label {
        662 +  .tour-interpretation p {
        663 +    margin: 0;
        664      color: var(--muted);
        665 +    line-height: 1.7;
        666 +  }
        667 +
        668 +  /* Coldness Test / Sentiment Timeline */
        669 +  .hypothesis-result {
        670 +    padding: 20px;
        671 +    border-radius: 12px;
        672 +    margin: 20px 0;
        673 +  }
        674 +
        675 +  .hypothesis-result.supports {
        676 +    background: rgba(16, 185, 129, 0.1);
        677 +    border: 1px solid rgba(16, 185, 129, 0.3);
        678 +  }
        679 +
        680 +  .hypothesis-result.challenges {
        681 +    background: rgba(239, 68, 68, 0.1);
        682 +    border: 1px solid rgba(239, 68, 68, 0.3);
        683 +  }
        684 +
        685 +  .hypothesis-verdict {
        686 +    font-size: 14px;
        687 +    font-weight: 700;
        688 +    letter-spacing: 0.05em;
        689 +  }
        690 +
        691 +  .supports .hypothesis-verdict {
        692 +    color: var(--success);
        693 +  }
        694 +
        695 +  .challenges .hypothesis-verdict {
        696 +    color: var(--danger);
        697 +  }
        698 +
        699 +  .hypothesis-detail p {
        700 +    margin: 8px 0;
        701 +    line-height: 1.6;
        702 +  }
        703 +
        704 +  .hypothesis-stats {
        705 +    display: flex;
        706 +    gap: 24px;
        707 +    margin-top: 12px;
        708 +    font-size: 13px;
        709 +    color: var(--muted);
        710 +  }
        711 +
        712 +  .coldness-chart {
        713 +    margin: 24px 0;
        714 +    padding: 20px;
        715 +    background: rgba(0, 0, 0, 0.2);
        716 +    border-radius: 12px;
        717 +  }
        718 +
        719 +  .coldness-chart svg {
        720 +    width: 100%;
        721 +    height: auto;
        722 +  }
        723 +
        724 +  .coldness-table {
        725 +    margin: 24px 0;
        726 +  }
        727 +
        728 +  .coldness-table h4 {
        729 +    margin: 0 0 16px;
        730 +  }
        731 +
        732 +  .coldness-rows {
        733 +    display: flex;
        734 +    flex-direction: column;
        735 +    gap: 10px;
        736 +  }
        737 +
        738 +  .coldness-row {
        739 +    display: grid;
        740 +    grid-template-columns: 12px 1fr 200px 60px;
        741 +    gap: 12px;
        742 +    align-items: center;
        743 +  }
        744 +
        745 +  .album-dot {
        746 +    width: 12px;
        747 +    height: 12px;
        748 +    border-radius: 50%;
        749 +  }
        750 +
        751 +  .coldness-album {
        752 +    font-size: 14px;
        753 +  }
        754 +
        755 +  .coldness-bar-container {
        756 +    height: 8px;
        757 +    background: rgba(0, 0, 0, 0.3);
        758 +    border-radius: 4px;
        759 +    position: relative;
        760 +  }
        761 +
        762 +  .coldness-bar-container::before {
        763 +    content: '';
        764 +    position: absolute;
        765 +    left: 50%;
        766 +    top: 0;
        767 +    bottom: 0;
        768 +    width: 1px;
        769 +    background: var(--border);
        770 +  }
        771 +
        772 +  .coldness-bar {
        773 +    height: 100%;
        774 +    border-radius: 4px;
        775 +    position: absolute;
        776 +    top: 0;
        777 +  }
        778 +
        779 +  .coldness-bar.warm {
        780 +    background: #60a5fa;
        781 +  }
        782 +
        783 +  .coldness-bar.cold {
        784 +    background: #ef4444;
        785 +  }
        786 +
        787 +  .coldness-value {
        788 +    font-size: 13px;
        789 +    font-weight: 600;
        790 +    text-align: right;
        791 +  }
        792 +
        793 +  .h4-section {
        794 +    margin-top: 32px;
        795 +    padding-top: 24px;
        796 +    border-top: 1px solid var(--border);
        797 +  }
        798 +
        799 +  .h4-section h4 {
        800 +    margin: 0 0 8px;
        801 +  }
        802 +
        803 +  .h4-desc {
        804 +    color: var(--muted);
        805 +    margin: 0 0 20px;
        806 +    line-height: 1.6;
        807 +  }
        808 +
        809 +  .warmth-comparison {
        810 +    display: flex;
        811 +    flex-direction: column;
        812 +    gap: 8px;
        813 +  }
        814 +
        815 +  .warmth-row {
        816 +    display: grid;
        817 +    grid-template-columns: 160px 1fr 60px;
        818 +    gap: 12px;
        819 +    align-items: center;
        820 +  }
        821 +
        822 +  .warmth-album {
        823 +    font-size: 13px;
        824 +  }
        825 +
        826 +  .warmth-bar-track {
        827 +    height: 8px;
        828 +    background: rgba(0, 0, 0, 0.3);
        829 +    border-radius: 4px;
        830 +    overflow: hidden;
        831 +  }
        832 +
        833 +  .warmth-bar-fill {
        834 +    height: 100%;
        835 +    border-radius: 4px;
        836 +  }
        837 +
        838 +  .warmth-value {
        839 +    font-size: 13px;
        840 +    font-weight: 600;
        841 +    text-align: right;
        842 +  }
        843 +
        844 +  /* Lyric Analyzer */
        845 +  .search-container {
        846 +    position: relative;
        847 +    margin: 20px 0;
        848 +  }
        849 +
        850 +  .search-input {
        851 +    width: 100%;
        852 +    padding: 14px 20px;
        853 +    background: rgba(0, 0, 0, 0.3);
        854 +    border: 1px solid var(--border);
        855 +    border-radius: 12px;
        856 +    color: var(--text);
        857 +    font-family: inherit;
        858 +    font-size: 16px;
        859 +  }
        860 +
        861 +  .search-input:focus {
        862 +    outline: none;
        863 +    border-color: var(--accent);
        864 +  }
        865 +
        866 +  .search-input::placeholder {
        867 +    color: var(--muted);
        868 +  }
        869 +
        870 +  .search-results {
        871 +    position: absolute;
        872 +    top: 100%;
        873 +    left: 0;
        874 +    right: 0;
        875 +    background: var(--panel);
        876 +    border: 1px solid var(--border);
        877 +    border-radius: 12px;
        878 +    margin-top: 4px;
        879 +    overflow: hidden;
        880 +    z-index: 10;
        881 +  }
        882 +
        883 +  .search-result {
        884 +    display: flex;
        885 +    justify-content: space-between;
        886 +    width: 100%;
        887 +    padding: 12px 20px;
        888 +    background: transparent;
        889 +    border: none;
        890 +    border-bottom: 1px solid var(--border);
        891 +    color: var(--text);
        892 +    font-family: inherit;
        893 +    cursor: pointer;
        894 +    text-align: left;
        895 +  }
        896 +
        897 +  .search-result:last-child {
        898 +    border-bottom: none;
        899 +  }
        900 +
        901 +  .search-result:hover {
        902 +    background: rgba(255, 255, 255, 0.05);
        903 +  }
        904 +
        905 +  .result-track {
        906 +    font-weight: 600;
        907 +  }
        908 +
        909 +  .result-album {
        910 +    color: var(--muted);
        911 +    font-size: 13px;
        912 +  }
        913 +
        914 +  .track-analysis {
        915 +    padding: 24px;
        916 +    background: rgba(0, 0, 0, 0.2);
        917 +    border: 2px solid var(--track-color, var(--border));
        918 +    border-radius: 12px;
        919 +    margin: 20px 0;
        920 +  }
        921 +
        922 +  .track-header {
        923 +    display: flex;
        924 +    justify-content: space-between;
        925 +    align-items: flex-start;
        926 +    margin-bottom: 24px;
        927 +  }
        928 +
        929 +  .track-header h3 {
        930 +    margin: 0;
        931 +    font-size: 24px;
        932 +  }
        933 +
        934 +  .track-album-info {
        935 +    color: var(--muted);
        936 +    margin: 4px 0 0;
        937 +  }
        938 +
        939 +  .close-btn {
        940 +    background: transparent;
        941 +    border: 1px solid var(--border);
        942 +    color: var(--muted);
        943 +    padding: 8px 16px;
        944 +    border-radius: 8px;
        945 +    cursor: pointer;
        946 +    font-family: inherit;
        947 +  }
        948 +
        949 +  .close-btn:hover {
        950 +    background: rgba(255, 255, 255, 0.05);
        951 +    color: var(--text);
        952 +  }
        953 +
        954 +  .analysis-grid {
        955 +    display: grid;
        956 +    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        957 +    gap: 20px;
        958 +    margin-bottom: 24px;
        959 +  }
        960 +
        961 +  .analysis-card {
        962 +    padding: 20px;
        963 +    background: rgba(0, 0, 0, 0.2);
        964 +    border-radius: 12px;
        965 +  }
        966 +
        967 +  .analysis-card h4 {
        968 +    margin: 0 0 16px;
        969 +    font-size: 14px;
        970 +    color: var(--muted);
        971 +    text-transform: uppercase;
        972 +    letter-spacing: 0.05em;
        973 +  }
        974 +
        975 +  .emotion-bars {
        976 +    display: flex;
        977 +    flex-direction: column;
        978 +    gap: 8px;
        979 +  }
        980 +
        981 +  .emotion-row {
        982 +    display: grid;
        983 +    grid-template-columns: 80px 1fr 40px;
        984 +    gap: 8px;
        985 +    align-items: center;
        986 +  }
        987 +
        988 +  .emotion-name {
        989      font-size: 12px;
        990 -    letter-spacing: 0.02em;
        990 +    text-transform: capitalize;
        991    }
        992
        993 -  .stat-value {
        993 +  .emotion-bar-track {
        994 +    height: 6px;
        995 +    background: rgba(0, 0, 0, 0.3);
        996 +    border-radius: 3px;
        997 +    overflow: hidden;
        998 +  }
        999 +
       1000 +  .emotion-bar-fill {
       1001 +    height: 100%;
       1002 +    border-radius: 3px;
       1003 +  }
       1004 +
       1005 +  .emotion-value {
       1006 +    font-size: 11px;
       1007 +    color: var(--muted);
       1008 +    text-align: right;
       1009 +  }
       1010 +
       1011 +  .temp-meter {
       1012 +    display: flex;
       1013 +    flex-direction: column;
       1014 +    gap: 12px;
       1015 +  }
       1016 +
       1017 +  .temp-scale {
       1018 +    display: flex;
       1019 +    justify-content: space-between;
       1020 +    font-size: 12px;
       1021 +  }
       1022 +
       1023 +  .temp-cold {
       1024 +    color: #60a5fa;
       1025 +  }
       1026 +
       1027 +  .temp-warm {
       1028 +    color: #ef4444;
       1029 +  }
       1030 +
       1031 +  .temp-bar-track {
       1032 +    height: 12px;
       1033 +    background: linear-gradient(90deg, #60a5fa, transparent 50%, #ef4444);
       1034 +    border-radius: 6px;
       1035 +    position: relative;
       1036 +  }
       1037 +
       1038 +  .temp-marker {
       1039 +    position: absolute;
       1040 +    top: -4px;
       1041 +    width: 4px;
       1042 +    height: 20px;
       1043 +    background: white;
       1044 +    border-radius: 2px;
       1045 +    transform: translateX(-50%);
       1046 +  }
       1047 +
       1048 +  .temp-values {
       1049 +    display: flex;
       1050 +    justify-content: space-between;
       1051 +  }
       1052 +
       1053 +  .temp-label {
       1054 +    display: block;
       1055 +    font-size: 11px;
       1056 +    color: var(--muted);
       1057 +  }
       1058 +
       1059 +  .temp-val {
       1060 +    font-weight: 600;
       1061 +  }
       1062 +
       1063 +  .stat-grid {
       1064 +    display: grid;
       1065 +    grid-template-columns: repeat(2, 1fr);
       1066 +    gap: 16px;
       1067 +  }
       1068 +
       1069 +  .stat-item {
       1070 +    text-align: center;
       1071 +  }
       1072 +
       1073 +  .stat-num {
       1074 +    display: block;
       1075 +    font-size: 28px;
       1076 +    font-weight: 700;
       1077 +    color: var(--track-color, var(--accent));
       1078 +  }
       1079 +
       1080 +  .stat-label {
       1081 +    font-size: 11px;
       1082 +    color: var(--muted);
       1083 +    text-transform: uppercase;
       1084 +  }
       1085 +
       1086 +  .lyrics-preview {
       1087 +    padding: 20px;
       1088 +    background: rgba(0, 0, 0, 0.2);
       1089 +    border-radius: 12px;
       1090 +  }
       1091 +
       1092 +  .lyrics-preview h4 {
       1093 +    margin: 0 0 12px;
       1094 +  }
       1095 +
       1096 +  .lyrics-text {
       1097 +    color: var(--muted);
       1098 +    line-height: 1.8;
       1099 +    font-style: italic;
       1100 +    margin: 0;
       1101 +  }
       1102 +
       1103 +  .standouts {
       1104 +    margin-top: 24px;
       1105 +  }
       1106 +
       1107 +  .standouts h4 {
       1108 +    margin: 0 0 16px;
       1109 +  }
       1110 +
       1111 +  .standout-grid {
       1112 +    display: grid;
       1113 +    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
       1114 +    gap: 20px;
       1115 +  }
       1116 +
       1117 +  .standout-category h5 {
       1118 +    margin: 0 0 12px;
       1119 +    font-size: 13px;
       1120 +    color: var(--accent);
       1121 +    text-transform: capitalize;
       1122 +  }
       1123 +
       1124 +  .standout-list {
       1125 +    display: flex;
       1126 +    flex-direction: column;
       1127 +    gap: 6px;
       1128 +  }
       1129 +
       1130 +  .standout-item {
       1131 +    display: flex;
       1132 +    align-items: center;
       1133 +    gap: 10px;
       1134 +    width: 100%;
       1135 +    padding: 10px 12px;
       1136 +    background: rgba(0, 0, 0, 0.2);
       1137 +    border: 1px solid var(--border);
       1138 +    border-radius: 8px;
       1139      color: var(--text);
       1140 +    font-family: inherit;
       1141 +    cursor: pointer;
       1142 +    text-align: left;
       1143 +  }
       1144 +
       1145 +  .standout-item:hover {
       1146 +    background: rgba(255, 255, 255, 0.05);
       1147 +  }
       1148 +
       1149 +  .standout-rank {
       1150 +    font-weight: 700;
       1151 +    color: var(--accent);
       1152 +    min-width: 20px;
       1153 +  }
       1154 +
       1155 +  .standout-track {
       1156 +    font-size: 13px;
       1157      font-weight: 600;
       1158 -    font-variant-numeric: tabular-nums;
       1158    }
       1159
       1160 +  .standout-album {
       1161 +    font-size: 11px;
       1162 +    color: var(--muted);
       1163 +    margin-left: auto;
       1164 +  }
       1165 +
       1166 +  .vocab-evolution {
       1167 +    margin-top: 32px;
       1168 +    padding-top: 24px;
       1169 +    border-top: 1px solid var(--border);
       1170 +  }
       1171 +
       1172 +  .vocab-evolution h4 {
       1173 +    margin: 0 0 8px;
       1174 +  }
       1175 +
       1176 +  .vocab-desc {
       1177 +    color: var(--muted);
       1178 +    margin: 0 0 20px;
       1179 +    line-height: 1.6;
       1180 +  }
       1181 +
       1182 +  .vocab-chart {
       1183 +    display: flex;
       1184 +    flex-direction: column;
       1185 +    gap: 8px;
       1186 +  }
       1187 +
       1188 +  .vocab-row {
       1189 +    display: grid;
       1190 +    grid-template-columns: 12px 160px 1fr 50px;
       1191 +    gap: 12px;
       1192 +    align-items: center;
       1193 +  }
       1194 +
       1195 +  .vocab-dot {
       1196 +    width: 12px;
       1197 +    height: 12px;
       1198 +    border-radius: 50%;
       1199 +  }
       1200 +
       1201 +  .vocab-album {
       1202 +    font-size: 13px;
       1203 +  }
       1204 +
       1205 +  .vocab-bar-track {
       1206 +    height: 8px;
       1207 +    background: rgba(0, 0, 0, 0.3);
       1208 +    border-radius: 4px;
       1209 +    overflow: hidden;
       1210 +  }
       1211 +
       1212 +  .vocab-bar-fill {
       1213 +    height: 100%;
       1214 +    border-radius: 4px;
       1215 +  }
       1216 +
       1217 +  .vocab-value {
       1218 +    font-size: 13px;
       1219 +    font-weight: 600;
       1220 +    text-align: right;
       1221 +  }
       1222 +
       1223 +  /* Footer */
       1224 +  .footer {
       1225 +    margin-top: 48px;
       1226 +    padding: 24px;
       1227 +    text-align: center;
       1228 +    border-top: 1px solid var(--border);
       1229 +  }
       1230 +
       1231 +  .footer p {
       1232 +    margin: 0;
       1233 +    color: var(--muted);
       1234 +    font-size: 13px;
       1235 +  }
       1236 +
       1237 +  /* Responsive */
       1238    @media (max-width: 720px) {
       1239 +    .hero {
       1240 +      flex-direction: column;
       1241 +    }
       1242 +
       1243 +    .hero-stats {
       1244 +      justify-content: flex-start;
       1245 +    }
       1246 +
       1247      .bar-row {
       1248        grid-template-columns: 1fr;
       1249      }
     ...
       211      .bar-value {
       212        text-align: left;
       213      }
       214 +
       215 +    .tlw-hero {
       216 +      flex-direction: column;
       217 +      text-align: center;
       218 +    }
       219 +
       220 +    .tour-stat-grid {
       221 +      flex-direction: column;
       222 +      gap: 16px;
       223 +    }
       224 +
       225 +    .nav-bar {
       226 +      flex-wrap: nowrap;
       227 +      overflow-x: auto;
       228 +      -webkit-overflow-scrolling: touch;
       229 +    }
       230    }

⏺ Let me test the web app builds correctly.

⏺ Bash(cd /Users/hussain/radiohead-lab/web && npm run build 2>&1 | tail -20)
⎿ > radiohead-lab-web@0.1.0 build > vite build
… +9 lines (ctrl+o to expand)

⏺ The web app builds successfully. Let me now generate the figures and update the todo.

⏺ Now let me create and run a script to generate the figures.

⏺ Read(~/radiohead-lab/src/visualization/album_trajectories.py)
⎿ Read 1 line

⏺ Write(~/radiohead-lab/src/visualization/generate_figures.py)
⎿ Wrote 304 lines to ../src/visualization/generate_figures.py  
 """
Generate static figures for Radiohead Data Lab analysis.
Outputs PNG files to results/figures/ for use in reports and documentation.
"""
from **future** import annotations
import json
import sys
… +294 lines (ctrl+o to expand)
⎿ Interrupted · What should Claude do instead?

> whts taking so long!

⏺ Sorry! Let me finish up quickly.

⏺ Bash(cd /Users/hussain/radiohead-lab && python src/visualization/generate_figures.py 2>&1)
⎿ Error: Exit code 1
Traceback (most recent call last):
File "/Users/hussain/radiohead-lab/src/visualization/generate_figures.py", line 18, in <module>
import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'

⏺ Matplotlib isn't installed - skipping figures. Here's what's done:
⎿ Interrupted · What should Claude do instead?

> I have Matplotlib with BREW. I'm on Python 3.13, so I tried to do it through BREW. I'm on PIP3.
> ⎿ Interrupted · What should Claude do instead?

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

> ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
> ⏵⏵ accept edits on (shift+tab to cycle) Context left until auto-compact: 11%
