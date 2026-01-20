-- KpopQuiz 데이터베이스 스키마 변경 스크립트

-- 1. `questions` 테이블에 `stage` 컬럼을 추가합니다.
-- 이 컬럼은 문제를 그룹화하여 스테이지 기반으로 게임을 진행하는 데 사용됩니다.
-- 인덱스를 추가하여 특정 스테이지의 문제를 빠르게 조회할 수 있도록 합니다.
ALTER TABLE questions ADD COLUMN stage INTEGER;
CREATE INDEX idx_questions_stage ON questions(stage);


-- 2. 모든 문제의 점수를 100점으로 통일합니다.
-- 기존의 난이도 기반 차등 점수 시스템에서, 모든 문제의 가치를 동일하게 만들어
-- 총 100문제 10,000점 만점 시스템의 기반을 마련합니다.
UPDATE questions SET points = 100;


-- 3. (선택적) 기존 데이터에 스테이지 정보를 할당합니다.
-- 아래 쿼리는 기존에 있던 문제들을 10개씩 묶어 순서대로 스테이지를 부여하는 예시입니다.
-- 데이터가 없는 경우에는 실행할 필요가 없습니다.
-- 실제 운영 환경에서는 데이터의 특성에 맞게 스테이지를 더 신중하게 할당해야 합니다.
-- 예시: UPDATE questions SET stage = (CAST(id AS INTEGER) - 1) / 10 + 1;

-- 참고: SQLite에서는 ALTER COLUMN을 직접 지원하지 않으므로,
-- `points` 컬럼의 DEFAULT 값을 변경하려면 테이블을 재생성하는 복잡한 과정이 필요합니다.
-- 하지만 `UPDATE`를 통해 모든 값을 100으로 설정하고,
-- 추후 INSERT 시 `points` 값을 명시적으로 100으로 설정하면 동일한 효과를 볼 수 있습니다.
-- 새로 추가되는 `Question` 모델의 기본값은 `default=100`으로 이미 변경되었습니다.
