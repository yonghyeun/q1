import type {
  ISODateTimeString,
  UnixMillis,
  UrlString,
  YouTubeChannelId,
  YouTubeVideoId,
} from "./primitives";

/**
 * 도메인 계약(contracts, SoT).
 *
 * 이 타입들은 `docs/product/glossary.md`의 유비쿼터스 언어(SoT)와
 * `docs/product/mvp-spec.md`의 MVP 데이터 모델 스케치를 최대한 반영한다.
 *
 * 규칙: analytics/storage와 키를 맞추기 위해 필드명은 `snake_case`를 우선한다.
 */
export const SOURCE_TYPES = ["channel"] as const;
/** 지원하는 Source 타입 유니온 (MVP: `channel`만). */
export type SourceType = (typeof SOURCE_TYPES)[number];

/** `Source`의 안정적 식별자(예: `channel:UCxxxx`). */
export type SourceId = `${SourceType}:${string}`;
/** `Note`의 안정적 식별자 (MVP: 1 Video : 1 Note). */
export type NoteId = `note:${string}`;
/** `Marker`의 안정적 식별자(노트 안 타임스탬프 레퍼런스). */
export type MarkerId = `marker:${string}`;

/** 유저가 영상을 여는 진입 방식. analytics의 `open_method`와 정렬한다. */
export const OPEN_METHODS = ["feed", "url", "note_list"] as const;
/** 지원하는 open method 유니온. */
export type OpenMethod = (typeof OPEN_METHODS)[number];

/** 피드 범위/필터 상태. glossary의 "All Feed" / "Channel Filter"와 정렬한다. */
export const FEED_FILTERS = ["all", "channel"] as const;
/** 지원하는 feed filter 유니온. */
export type FeedFilter = (typeof FEED_FILTERS)[number];

/** 타임스탬프 레퍼런스를 노트에 삽입한 방식. analytics의 `method`와 정렬한다. */
export const TIMESTAMP_INSERT_METHODS = ["hotkey", "button", "auto"] as const;
/** 지원하는 timestamp insertion method 유니온. */
export type TimestampInsertMethod = (typeof TIMESTAMP_INSERT_METHODS)[number];

/**
 * Glossary Entity: ChannelSource
 *
 * 유저가 YouTube 채널 URL로 등록하는 학습 Source.
 */
export interface ChannelSource {
  source_id: SourceId;
  source_type: "channel";
  source_url: UrlString;
  channel_id: YouTubeChannelId;
  added_at: UnixMillis;
}

/** Glossary Entity: Source (MVP: `ChannelSource`만). */
export type Source = ChannelSource;

/**
 * Glossary Entity: Video
 *
 * `video_id` + UI에 필요한 최소 메타데이터로 표현되는 YouTube 영상.
 */
export interface Video {
  video_id: YouTubeVideoId;
  channel_id: YouTubeChannelId;
  published_at: ISODateTimeString;
  title: string;
  thumbnail_url?: UrlString;
}

/** 피드 목록에서 사용하는 Video 형태 (MVP에서는 `Video`와 동일). */
export type VideoSummary = Video;

/** 캐시/메타데이터 용도의 Video 형태 (MVP에서는 `Video`와 동일). */
export type VideoMetadata = Video;

/**
 * 앱에서 "유저가 영상을 열었다"라는 기록.
 *
 * (선택) "최근 열어본 영상" 같은 UX에 사용하며 analytics와도 정렬 가능하다.
 */
export interface VideoOpenRecord {
  video_id: YouTubeVideoId;
  open_method: OpenMethod;
  opened_at: UnixMillis;
  source_id?: SourceId;
  feed_filter?: FeedFilter;
  filter_source_id?: SourceId;
}

/**
 * Glossary Entity: Note
 *
 * MVP 제약: 1 Video : 1 Note. 내용은 Markdown으로 저장한다.
 */
export interface Note {
  note_id: NoteId;
  video_id: YouTubeVideoId;
  markdown: string;
  created_at: UnixMillis;
  updated_at: UnixMillis;
}

/**
 * Glossary Entity: Marker
 *
 * Note 안에 삽입되는 타임스탬프 레퍼런스.
 * - 저장: 정수 초(`timestamp_seconds`)
 * - 표시: `HH:MM:SS`
 * - 클릭: 외부 이동이 아니라 임베드 플레이어 `seek`으로 동작
 */
export interface Marker {
  marker_id: MarkerId;
  note_id: NoteId;
  /** 영상 시작 기준 정수 초. */
  timestamp_seconds: number;
  text?: string;
  created_at: UnixMillis;
}

/** Video Feed UI 상태(필터 + 선택된 채널). */
export interface VideoFeedState {
  feed_filter: FeedFilter;
  filter_source_id?: SourceId;
}

/**
 * 표시 목적의 YouTube 채널 메타데이터.
 *
 * 주의: YouTube API에서 온 데이터다. `docs/product/youtube-api-policy-notes.md`를 참고하고,
 * 장기 저장보다는 TTL 캐시를 기본으로 한다.
 */
export interface ChannelMetadata {
  channel_id: YouTubeChannelId;
  title: string;
  thumbnail_url?: UrlString;
}
